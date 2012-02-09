######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import logging
log = logging.getLogger("zen.useraction.actions")
from copy import copy

import Globals

from zope.interface import implements

from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenUtils.ProcessQueue import ProcessQueue

from Products.ZenModel.interfaces import IAction, IProvidesEmailAddresses
from Products.ZenModel.actions import CommandAction, EventCommandProtocol, \
     processTalSource, _signalToContextDict

from ZenPacks.zenoss.Notifications.interfaces import IUserCommandActionContentInfo


class UserCommandAction(CommandAction):
    implements(IAction)

    id = 'user_command'
    name = 'User Command'
    actionContentInfo = IUserCommandActionContentInfo

    shouldExecuteInBatch = True

    def configure(self, options):
        super(CommandAction, self).configure(options)
        self.processQueue = ProcessQueue(options.get('maxCommands', 10))
        self.processQueue.start()

    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)

    def executeBatch(self, notification, signal, targets):
        self.setupAction(notification.dmd)

        log.debug('Executing action: Command')

        if signal.clear:
            command = notification.content['clear_body_format']
        else:
            command = notification.content['body_format']

        log.debug('Executing this command: %s' % command)

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


        for target in targets:
            self.executeSingleTarget(command, environ, notification, target)

    def executeSingleTarget(self, command, environ, notification, target):
        environcopy = copy(environ)
        environcopy.update( {'user':target, 'group':target} )
        command = processTalSource(command, **environcopy)
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
        if IProvidesEmailAddresses.providedBy(target):
            return target

    def updateContent(self, content=None, data=None):
        super(UserCommandAction, self).updateContent(content, data)

        updates = dict()
        properties = ['user_env_format']
        for k in properties:
            updates[k] = data.get(k)

        content.update(updates)

