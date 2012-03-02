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

