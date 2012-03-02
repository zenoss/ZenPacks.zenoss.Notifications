===============================================================================
ZenPacks.zenoss.Notifications
===============================================================================


About
-------------------------------------------------------------------------------
This ZenPack adds new event notification actions that are used by the
``zenactiond`` daemon.


Features
-------------------------------------------------------------------------------

The following event notification actions have been added:

Alternate Email Host

    This action allows for different email servers to be defined as
    destinations, rather than just the ``Advanced`` -> ``Settings`` email
    definition.

Configurable SNMP Trap

    This action allows for the port, community string, and SNMP protocol version
    to be specified.

User Command
    
    This action allows for environment variables to be set, and also allows per-
    user information to be extracted using TALES expressions.


Prerequisites
-------------------------------------------------------------------------------

==================  =========================================================
Prerequisite        Restriction
==================  =========================================================
Product             Zenoss 4.1.1 or higher
Required ZenPacks   None
Other dependencies  None
==================  =========================================================


Limitations
-------------------------------------------------------------------------------
These notification actions are not able to provide immediate feedback as to
whether or not configuration information is correct, so the ``zenactiond.log``
file must be checked to ensure that the actions are working correctly.


Usage
-------------------------------------------------------------------------------
See the Zenoss Service Dynamics Administration Guide for more information about
triggers and notifications. Any issues detected during the run of the
notification will result in an event sent to the event console as well as a
message in the ``zenactiond.log`` file.


Select the Alternate Email Host Action
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This assumes that the appropriate triggers have already been set up.

    1. Navigate to ``Events`` -> ``Triggers`` page.

    2. Click on the ``Notifications`` menu item.

    3. Click on the plus sign ('+') to add a new notification.

    4. From the dialog box, specify the name of the notification and select
       the``Alternate Email Host`` action.

    5. Enable the notification and add a trigger to be associated with this
       action.

    6. Click on the ``Contents`` tab.

    7. Fill in the settings for the email server, which are the same type as
       found on the ``Advanced`` -> ``Settings`` page.

    8. Click on the ``Submit`` button.


Select the Configurable SNMP Trap Action
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This assumes that the appropriate triggers have already been set up.
   
    1. Navigate to ``Events`` -> ``Triggers`` page.

    2. Click on the ``Notifications`` menu item.

    3. Click on the plus sign ('+') to add a new notification.

    4. From the dialog box, specify the name of the notification and select the
       ``Configurable SNMP Trap`` action.

    5. Enable the notification and add a trigger to be associated with this
       action.

    6. Click on the ``Contents`` tab.

    7. Fill in the settings for the SNMP receiver: host, port, community string,
       and SNMP version.

    8. Click on the ``Submit`` button.


Select the User Command Action
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This assumes that the appropriate triggers have already been set up.
   
    1. Navigate to ``Events`` -> ``Triggers`` page.

    2. Click on the ``Notifications`` menu item.

    3. Click on the plus sign ('+') to add a new notification.

    4. From the dialog box, specify the name of the notification and select the
       ``User Command`` action.

    5. Enable the notification and add a trigger to be associated with this
       action.

    6. Click on the ``Contents`` tab.

    7. Fill in the command for the commands. Note that the ``user`` variable is
       available, and that environment variables can be specified. Environment
       variables are semi-colon separated and consist of ``NAME=value`` items.

    8. Click on the ``Submit`` button.


Installing
-------------------------------------------------------------------------------

Install the ZenPack via the command line and restart Zenoss::

    zenpack --install ZenPacks.zenoss.Notifications-<version>.egg
    zenoss restart


Removing
-------------------------------------------------------------------------------

To remove the ZenPack, use the following command::

    zenpack --remove ZenPacks.zenoss.Notifications
    zenoss restart


Troubleshooting
-------------------------------------------------------------------------------

The Zenoss support team will need the following output:

    1. Set the ``zenhub`` daemon into ``DEBUG`` level logging by typing
       ``zenhub debug`` from the command-line. This will ensure that we can see
       the incoming event in the ``zenhub.log`` file.

    2. Set the ``zenactiond`` daemon into ``DEBUG`` level logging by typing
       ``zenactiond debug`` from the command-line. This will ensure that we can
       see the incoming notification request and processing activity in the
       ``zenactiond.log`` file.

    3. Create an event from the remote source, by the ``zensendevent`` command
       or by the event console ``Add an Event`` button. This event must match
       the trigger definition that will invoke your notification action.

    4. Verify that the event was processed by the ``zenhub`` daemon by examining
       the ``zenhub.log`` file.

    5. Wait for the ``zenactiond`` daemon to receive and then process the
       notification request.

    6. In the case of errors an event will be generated and sent to the event
       console.


Appendix Related Daemons
-------------------------------------------------------------------------------

============  ===============================================================
Type          Name
============  ===============================================================
Notification  zenactiond
============  ===============================================================
