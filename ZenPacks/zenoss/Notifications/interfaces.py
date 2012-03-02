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

import Globals

from zope.schema.vocabulary import SimpleVocabulary

from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.Zuul.interfaces.actions import (
   ICommandActionContentInfo, IEmailActionContentInfo,
   ISnmpTrapActionContentInfo,
)


class IUserCommandActionContentInfo(ICommandActionContentInfo):

    user_env_format = schema.Text(
        title       = _t(u'Environment variables'),
        description = _t(u'A semi-colon separated list of environment variables.'),
    )


class IAltEmailHostActionContentInfo(IEmailActionContentInfo):

    email_from = schema.Text(
        title       = _t(u'From Address for Emails'),
        description = _t(u'The user from which the e-mail originated on the Zenoss server.'),
        default = u'root@localhost.localdomain'
    )

    host = schema.Text(
        title       = _t(u'SMTP Host'),
        description = _t(u'Simple Mail Transport Protocol (aka E-mail server).'),
    )

    port = schema.Int(
        title       = _t(u'SMTP Port (usually 25)'),
        description = _t(u'TCP/IP port to access Simple Mail Transport Protocol (aka E-mail server).'),
        default = 25
    )

    useTls = schema.Bool(
        title       = _t(u'Use TLS?'),
        description = _t(u'Use Transport Layer Security for E-mail?'),
        default = False
    )

    user = schema.Text(
        title       = _t(u'SMTP Username (blank for none)'),
        description = _t(u'Use this only if authentication is required.'),
    )

    password = schema.Password(
        title       = _t(u'SMTP Password (blank for none)'),
        description = _t(u'Use this only if authentication is required.'),
    )


class IConfigurableSnmpTrapActionContentInfo(ISnmpTrapActionContentInfo):

    community = schema.Text(
        title       = _t(u'SNMP Community'),
        description = _t(u'SNMP authentication string.'),
        default = _t(u'public')
    )

    version = schema.Choice(
        title       = _t(u'SNMP Version'),
        description = _t(u'SNMP trap protocol version.'),
        vocabulary  = SimpleVocabulary.fromValues(['v1', 'v2c']),
        default = _t(u'v1')
    )

    port = schema.Int(
        title       = _t(u'SNMP Port (usually 162)'),
        description = _t(u'Port number used by the SNMP trap receiver process.'),
        default = 162
    )

