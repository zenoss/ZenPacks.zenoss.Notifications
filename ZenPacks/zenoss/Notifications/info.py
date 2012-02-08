######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################


import Globals

from zope.interface import implements

from Products.Zuul.infos.actions import CommandActionContentInfo, ActionFieldProperty

from ZenPacks.zenoss.Notifications.interfaces import IUserCommandActionContentInfo


class UserActionContentInfo(CommandActionContentInfo):
    implements(IUserCommandActionContentInfo)

    user_env_format = ActionFieldProperty(IUserCommandActionContentInfo, 'user_env_format')


