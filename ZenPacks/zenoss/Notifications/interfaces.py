######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import Globals

from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.Zuul.interfaces.actions import (
   ICommandActionContentInfo, IEmailActionContentInfo
)


class IUserCommandActionContentInfo(ICommandActionContentInfo):

    user_env_format = schema.Text(
        title       = _t(u'Environment variables'),
        description = _t(u'A semi-colon separated list of environment variables.'),
    )


class IAltEmailHostActionContentInfo(IEmailActionContentInfo):

    email_from = schema.Text(
        title       = _t(u'From Address for Emails'),
        description = _t(u'Defaults to Advanced -> Settings values.')
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

    password = schema.Text(
        title       = _t(u'SMTP Password (blank for none)'),
        description = _t(u'Use this only if authentication is required.'),
    )

