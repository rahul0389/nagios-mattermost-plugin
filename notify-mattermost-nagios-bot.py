#!/usr/bin/env python
#    Copyright (C) 2020 Rahul Lamba
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import requests

VERSION = "0.0.1"


def parse():
    parser = argparse.ArgumentParser(description='Sends alerts to Mattermost based on the bot.')
    parser.add_argument('--url', help='API URL', required=True)
    parser.add_argument('--channel', help='Channel to notify', required=True)
    parser.add_argument('--username', help='Username to notify as',
                        default='Nagios')
    parser.add_argument('--iconurl', help='URL of icon to use for username',
                        default='https://slack.global.ssl.fastly.net/7bf4/img/services/nagios_128.png') # noqa
    parser.add_argument('--notificationtype', help='Notification Type',
                        required=True)
    parser.add_argument('--authorizationtoken', help='Access Token', required=True)
    parser.add_argument('--hostalias', help='Host Alias', required=True)
    parser.add_argument('--hostaddress', help='Host Address', required=True)
    parser.add_argument('--hoststate', help='Host State')
    parser.add_argument('--hostoutput', help='Host Output')
    parser.add_argument('--servicedesc', help='Service Description')
    parser.add_argument('--servicestate', help='Service State')
    parser.add_argument('--serviceoutput', help='Service Output')
    parser.add_argument('--cgiurl', help='Link to extinfo.cgi on your Nagios instance')
    parser.add_argument('--version', action='version',
                        version='% (prog)s {version}'.format(version=VERSION))
    args = parser.parse_args()
    return args


def encode_special_characters(text):
    text = text.replace("%", "%25")
    text = text.replace("&", "%26")
    return text


def emoji(notificationtype):
    return {
        "CUSTOM": ":fire: ",
        "RECOVERY": ":white_check_mark: ",
        "PROBLEM": ":fire: ",
        "DOWNTIMESTART": ":clock10: ",
        "DOWNTIMEEND": ":sunny: "
    }.get(notificationtype, "")


def text(args):
    template_host = "__{notificationtype}__ {hostalias} is {hoststate}\n{hostoutput}"
    template_service = "__{notificationtype}__ {hostalias} at {hostaddress}/{servicedesc} is {servicestate}\n{serviceoutput}" # noqa
    if args.hoststate is not None:
        template_cgiurl = " [View :link:]({cgiurl}?type=1&host={hostalias})"
    elif args.servicestate is not None:
        template_cgiurl = " [View :link:]({cgiurl}?type=2&host={hostalias}&service={servicedesc})"
    template = template_service if args.servicestate else template_host

    text = emoji(args.notificationtype) + template.format(**vars(args))
    if args.cgiurl is not None:
        # If we know the CGI url provide a clickable link to the nagios CGI
        text = text + template_cgiurl.format(**vars(args))
    return encode_special_characters(text)


if __name__ == "__main__":
    args = parse()
    token = 'Bearer '+args.authorizationtoken
    url = args.url
    channelId = args.channel
    hed = {'Authorization': token, 'Content-Type': 'application/json'}
    data = {"channel_id": channelId, "message": text(args)}
    response = requests.post(url, json.dumps(data), headers=hed)