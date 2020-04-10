# nagios-mattermost-plugin
A plugin for Nagios and other compatible software to enable notifications to a Mattermost server.

## Create Bot in Mattermost
1. Go to Main Menu > Integrations > Bot Accounts.
2. Click Add Bot Account.
3. Set the Username of the bot. The username must begin with a letter, and contain between 3 and 22 lowercase characters made up of numbers, letters, and the symbols “.”, “-“, and “_”.
(Optional) Upload an image for the Bot Icon. This will be used as the profile image of the bot throughout the Mattermost user interface.
(Optional) Set a Display Name and Description.
(Optional) Choose what role the bot should have. Defaults to Member. If you assign System Admin, the bot will have access to write in and read any public channels, private channels and direct messages.
(Optional) Select additional permissions for the account. Enable the bot to post to all Mattermost channels, or all Mattermost public channels.

## Nagios Configuration

The steps below are for a Nagios xi server but should work with minimal modifications for compatible software:

1. Copy `mattermost.py` to `/usr/local/nagios/libexec`.

2. Create a *Nagios Bot*  for the approriate team.

3. Create the command definitions in your Nagios configuration:

    ```
    define command {
        command_name notify-service-by-mattermost
        command_line /usr/local/nagios/libexec/mattermost.py --url [MATTERMOST-API-URL] \
                                                             --channel [MATTERMOST-CHANNEL-ID] \
                                                             --notificationtype "$NOTIFICATIONTYPE$" \
                                                             --hostalias "$HOSTNAME$" \
                                                             --hostaddress "$HOSTADDRESS$" \
                                                             --servicedesc "$SERVICEDESC$" \
                                                             --servicestate "$SERVICESTATE$" \
                                                             --serviceoutput "$SERVICEOUTPUT$"
    }

    define command {
        command_name notify-host-by-mattermost
        command_line /usr/local/nagios/libexec/mattermost.py --url [MATTERMOST-API-URL] \
                                                             --channel [MATTERMOST-CHANNEL-ID] \
                                                             --notificationtype "$NOTIFICATIONTYPE$" \
                                                             --hostalias "$HOSTNAME$" \
                                                             --hostaddress "$HOSTADDRESS$" \
                                                             --hoststate "$HOSTSTATE$" \
                                                             --hostoutput "$HOSTOUTPUT$"
    }
```

4. Create the contact definition in your Nagios configuration:

    ```
    define contact {
        contact_name                            mattermost
        alias                                   Mattermost
        service_notification_period             24x7
        host_notification_period                24x7
        service_notification_options            w,u,c,r
        host_notification_options               d,r
        host_notification_commands              notify-host-by-mattermost
        service_notification_commands           notify-service-by-mattermost
    }
```

5. Add the contact to a contact group in your Nagios configuration:

    ```
    define contactgroup{
        contactgroup_name       network-admins
        alias                   Network Administrators
        members                 email, mattermost
    }
```
