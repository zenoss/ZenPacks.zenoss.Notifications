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

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate

from Products.ZenUtils.Utils import sendEmail
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import EmailAction, \
     processTalSource, _signalToContextDict, ActionExecutionException

from ZenPacks.zenoss.Notifications.interfaces import IAltEmailHostActionContentInfo


class AltEmailHostAction(EmailAction):
    implements(IAction)

    id = 'altemailhost'
    name = 'Alternate Email Host'
    actionContentInfo = IAltEmailHostActionContentInfo

    def executeBatch(self, notification, signal, targets):
        log.debug("Executing %s action for targets: %s", self.name, targets)
        self.setupAction(notification.dmd)

        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)
        if signal.clear:
            log.debug('This is a clearing signal.')
            subject = processTalSource(notification.content['clear_subject_format'], **data)
            body = processTalSource(notification.content['clear_body_format'], **data)
        else:
            subject = processTalSource(notification.content['subject_format'], **data)
            body = processTalSource(notification.content['body_format'], **data)

        log.debug('Sending this subject: %s' % subject)
        log.debug('Sending this body: %s' % body)

        plain_body = MIMEText(self._stripTags(body))
        email_message = plain_body

        if notification.content['body_content_type'] == 'html':
            email_message = MIMEMultipart('related')
            email_message_alternative = MIMEMultipart('alternative')
            email_message_alternative.attach(plain_body)

            html_body = MIMEText(body.replace('\n', '<br />\n'))
            html_body.set_type('text/html')
            email_message_alternative.attach(html_body)

            email_message.attach(email_message_alternative)

        host = notification.content['host']
        port = notification.content['port']
        user = notification.content['user']
        password = notification.content['password']
        useTls = notification.content['useTls']
        email_from = notification.content['email_from']

        email_message['Subject'] = subject
        email_message['From'] = email_from
        email_message['To'] = ','.join(targets)
        email_message['Date'] = formatdate(None, True)

        result, errorMsg = sendEmail(
            email_message,
            host, port,
            useTls,
            user, password
        )

        if result:
            log.debug("Notification '%s' sent emails to: %s",
                     notification.id, targets)
        else:
            raise ActionExecutionException(
                "Notification '%s' FAILED to send emails to %s: %s" %
                (notification.id, targets, errorMsg)
            )

    def updateContent(self, content=None, data=None):
        super(AltEmailHostAction, self).updateContent(content, data)

        updates = dict()
        properties = ['host', 'port', 'user', 'password', 'useTls', 'email_from']
        for k in properties:
            updates[k] = data.get(k)

        content.update(updates)

