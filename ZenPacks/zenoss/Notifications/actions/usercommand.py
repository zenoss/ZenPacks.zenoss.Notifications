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

import Globals

from zope.interface import implements

from Products.ZenModel.UserSettings import GroupSettings
from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenUtils.ProcessQueue import ProcessQueue

from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import IActionBase, TargetableAction, EventCommandProtocol, \
     processTalSource, _signalToContextDict, ActionExecutionException

from ZenPacks.zenoss.Notifications.interfaces import IUserCommandActionContentInfo


class UserCommandAction(IActionBase, TargetableAction):
    implements(IAction)

    id = 'user_command'
    name = 'User Command'
    actionContentInfo = IUserCommandActionContentInfo

    shouldExecuteInBatch = False

    def configure(self, options):
        super(UserCommandAction, self).configure(options)
        self.processQueue = ProcessQueue(options.get('maxCommands', 10))
        self.processQueue.start()

    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)
        self.dmd = dmd

    def executeOnTarget(self, notification, signal, target):
        self.setupAction(notification.dmd)

        log.debug('Executing action: %s on %s', self.name, target)

        if signal.clear:
            command = notification.content['clear_body_format']
        else:
            command = notification.content['body_format']

        log.debug('Executing this command: %s', command)

        actor = signal.event.occurrence[0].actor
        device = None
        if actor.element_uuid:
            device = self.guidManager.getObject(actor.element_uuid)

        component = None
        if actor.element_sub_uuid:
            component = self.guidManager.getObject(actor.element_sub_uuid)

        user_env_format = notification.content['user_env_format']
        env = dict( envvar.split('=') for envvar in user_env_format.split(';') if '=' in envvar)

        environ = {'dev': device, 'component': component, 'dmd': notification.dmd,
                   'env': env}
        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)
        environ.update(data)

        if environ.get('evt', None):
            environ['evt'] = self._escapeEvent(environ['evt'])

        if environ.get('clearEvt', None):
            environ['clearEvt'] = self._escapeEvent(environ['clearEvt'])

        environ['user'] = getattr(self.dmd.ZenUsers, target, None)

        try:
            command = processTalSource(command, **environ)
        except Exception:
            raise ActionExecutionException('Unable to perform TALES evaluation on "%s" -- is there an unescaped $?' % command)

        log.debug('Executing this compiled command: "%s"' % command)
        _protocol = EventCommandProtocol(command)

        log.debug('Queueing up command action process.')
        self.processQueue.queueProcess(
            '/bin/sh',
                ('/bin/sh', '-c', command),
            env=environ['env'],
            processProtocol=_protocol,
            timeout=int(notification.content['action_timeout']),
            timeout_callback=_protocol.timedOut
        )

    def getActionableTargets(self, target):
        ids = [target.id]
        if isinstance(target, GroupSettings):
            ids = [x.id for x in target.getMemberUserSettings()]
        return ids

    def updateContent(self, content=None, data=None):
        updates = dict()

        properties = ['body_format', 'clear_body_format', 'action_timeout', 
                      'user_env_format']
        for k in properties:
            updates[k] = data.get(k)

        content.update(updates)

    def _escapeEvent(self, evt):
        """
        Escapes the relavent fields of an event context for event commands.
        """
        if evt.message:
            evt.message = self._wrapInQuotes(evt.message)
        if evt.summary:
            evt.summary = self._wrapInQuotes(evt.summary)
        return evt

    def _wrapInQuotes(self, msg):
        """
        Wraps the message in quotes, escaping any existing quote.

        Before:  How do you pronounce "Zenoss"?
        After:  "How do you pronounce \"Zenoss\"?"
        """
        QUOTE = '"'
        BACKSLASH = '\\'
        return ''.join((QUOTE, msg.replace(QUOTE, BACKSLASH + QUOTE), QUOTE))

