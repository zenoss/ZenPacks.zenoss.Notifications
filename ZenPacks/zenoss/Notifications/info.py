######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################


import Globals

from zope.interface import implements

from Products.Zuul.infos.actions import (
      CommandActionContentInfo, EmailActionContentInfo, ActionFieldProperty,
      SnmpTrapActionContentInfo,
)

from ZenPacks.zenoss.Notifications.interfaces import (
    IUserCommandActionContentInfo, IAltEmailHostActionContentInfo,
    IConfigurableSnmpTrapActionContentInfo
)


class UserActionContentInfo(CommandActionContentInfo):
    implements(IUserCommandActionContentInfo)

    user_env_format = ActionFieldProperty(IUserCommandActionContentInfo, 'user_env_format')


class AltEmailHostActionContentInfo(EmailActionContentInfo):
    implements(IAltEmailHostActionContentInfo)

    email_from = ActionFieldProperty(IAltEmailHostActionContentInfo, 'email_from')
    host = ActionFieldProperty(IAltEmailHostActionContentInfo, 'host')
    port = ActionFieldProperty(IAltEmailHostActionContentInfo, 'port')
    useTls = ActionFieldProperty(IAltEmailHostActionContentInfo, 'useTls')
    user = ActionFieldProperty(IAltEmailHostActionContentInfo, 'user')
    password = ActionFieldProperty(IAltEmailHostActionContentInfo, 'password')


class ConfigurableSnmpTrapActionContentInfo(SnmpTrapActionContentInfo):
    implements(IConfigurableSnmpTrapActionContentInfo)

    community = ActionFieldProperty(IConfigurableSnmpTrapActionContentInfo, 'community')
    version = ActionFieldProperty(IConfigurableSnmpTrapActionContentInfo, 'version')
    port = ActionFieldProperty(IConfigurableSnmpTrapActionContentInfo, 'port')

