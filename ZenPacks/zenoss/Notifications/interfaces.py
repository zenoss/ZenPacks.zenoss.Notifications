######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import Globals

from zope.interface import Interface

from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.Zuul.interfaces.actions import ICommandActionContentInfo


class IUserCommandActionContentInfo(ICommandActionContentInfo):

    user_env_format = schema.Text(
        title       = _t(u'Environment variables'),
        description = _t(u'A semi-colon separated list of environment variables.')
    )


