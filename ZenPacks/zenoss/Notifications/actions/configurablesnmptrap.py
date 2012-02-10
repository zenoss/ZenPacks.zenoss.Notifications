######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import logging
log = logging.getLogger("zen.useraction.actions")

import Globals

from zope.interface import implements

from pynetsnmp import netsnmp

from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import SNMPTrapAction, _signalToContextDict

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

        varbinds = []
        for field, oidspec in sorted(fields.items(), key=lambda x: x[1][0]):
            i, source = oidspec
            if source == event.details:
                val = source.get(field, '')
            else:
                val = getattr(source, field, '')
            if isinstance(val, (list, tuple, set)):
                val = '|'.join(val)
            varbinds.append(("%s.%d" % (baseOID,i), 's', str(val)))

        session = self._getSession(notification.content)
        if session is not None:
            self.postProcessVarBinds(varbinds, notification.dmd)
            session.sendTrap(baseOID + '.0.0.1', varbinds=varbinds)

    def updateContent(self, content=None, data=None):
        content['action_destination'] = data.get('action_destination')
        content['community'] = data.get('community')
        content['version'] = data.get('version')
        content['port'] = data.get('port')

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
            session = netsnmp.Session((
                '-%s' % version,
                '-c', community,
                '%s:%' % (traphost, port))
            )
            # FIXME: What happens if the IP isn't reachable or is insane?
            session.open()
            self._sessions[destination] = session

        return session

    def postProcessVarBinds(self, varbinds, dmd):
        pass

