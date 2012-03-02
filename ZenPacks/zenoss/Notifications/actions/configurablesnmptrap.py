###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2012, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import logging
log = logging.getLogger("zen.useraction.actions")
from socket import getaddrinfo

import Globals

from zope.interface import implements

from pynetsnmp import netsnmp

from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import SNMPTrapAction, _signalToContextDict, ActionExecutionException


from ZenPacks.zenoss.Notifications.interfaces import IConfigurableSnmpTrapActionContentInfo


class ConfigurableSnmpTrapAction(SNMPTrapAction):
    implements(IAction)

    id = 'configurabletrapaction'
    name = 'Configurable SNMP Trap'
    actionContentInfo = IConfigurableSnmpTrapActionContentInfo

    _sessions = {}

    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)

    def execute(self, notification, signal):
        """
        Send out an SNMP trap according to the definition in ZENOSS-MIB.
        """
        log.debug('Processing %s Trap action.', self.name)
        self.setupAction(notification.dmd)

        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)
        event = data['eventSummary']
        actor = event.actor
        details = event.details

        baseOID = '1.3.6.1.4.1.14296.1.100'

        fields = {
           'uuid' :                         ( 1, event),
           'fingerprint' :                  ( 2, event),
           'element_identifier' :           ( 3, actor),
           'element_sub_identifier' :       ( 4, actor),
           'event_class' :                  ( 5, event),
           'event_key' :                    ( 6, event),
           'summary' :                      ( 7, event),
           'message' :                      ( 8, event),
           'severity' :                     ( 9, event),
           'status' :                       (10, event),
           'event_class_key' :              (11, event),
           'event_group' :                  (12, event),
           'state_change_time' :            (13, event),
           'first_seen_time' :              (14, event),
           'last_seen_time' :               (15, event),
           'count' :                        (16, event),
           'zenoss.device.production_state':(17, details),
           'agent':                         (20, event),
           'zenoss.device.device_class':    (21, details),
           'zenoss.device.location' :       (22, details),
           'zenoss.device.systems' :        (23, details),
           'zenoss.device.groups' :         (24, details),
           'zenoss.device.ip_address':      (25, details),
           'syslog_facility' :              (26, event),
           'syslog_priority' :              (27, event),
           'nt_event_code' :                (28, event),
           'current_user_name' :            (29, event),
           'cleared_by_event_uuid' :        (31, event),
           'zenoss.device.priority' :       (32, details),
           'event_class_mapping_uuid':      (33, event)
           }

        eventDict = self.creatEventDict(fields, event)
        self.processEventDict(eventDict, data, notification.dmd)
        varbinds = self.makeVarBinds(baseOID, fields, eventDict)

        session = self._getSession(notification.content)
        session.sendTrap(baseOID + '.0.0.1', varbinds=varbinds)

    def creatEventDict(self, fields, event):
        """
        Create an event dictionary suitable for Python evaluation.
        """
        eventDict = {}
        for field, oidspec in fields.items():
            i, source = oidspec
            if source == event.details:
                val = source.get(field, '')
            else:
                val = getattr(source, field, '')
            eventDict[field] = val
        return eventDict

    def processEventDict(self, eventDict, data, dmd):
        """
        Integration hook
        """
        pass

    def makeVarBinds(self, baseOID, fields, eventDict):
        """
        Make the SNMP variable bindings in numeric order.
        """
        intValues = (9, 10, 26, 27)
        varbinds = []
        for field, oidspec in sorted(fields.items(), key=lambda x: x[1][0]):
            i, source = oidspec
            val = eventDict.get(field, '')
            if isinstance(val, (list, tuple, set)):
                val = '|'.join(val)

            # Create the binding
            oid = "%s.%d" % (baseOID, i)
            oidType = 's' if i not in intValues else 'i'
            # No matter what the OID data type, send in strings as that's what is expected
            val = str(val)

            varbinds.append( (oid, oidType, val) )
        return varbinds

    def updateContent(self, content=None, data=None):
        content['action_destination'] = data.get('action_destination')
        content['community'] = data.get('community')
        content['version'] = data.get('version')
        content['port'] = int(data.get('port'))

    def _getSession(self, content):
        traphost = content['action_destination']
        port = content['port']
        destination = '%s:%s' % (traphost, port)

        if not traphost or port <= 0:
            log.error("%s: SNMP trap host information %s is incorrect ", destination)
            return None

        community = content['community']
        version = content['version']

        session = self._sessions.get(destination, None)
        if session is None:
            log.debug("Creating SNMP trap session to %s", destination)

            # Test that the hostname and port are sane.
            try:
                getaddrinfo(traphost, port)
            except Exception:
                raise ActionExecutionException("The destination %s is not resolvable." % destination)

            session = netsnmp.Session((
                '-%s' % version,
                '-c', community,
                destination)
            )
            session.open()
            self._sessions[destination] = session

        return session

