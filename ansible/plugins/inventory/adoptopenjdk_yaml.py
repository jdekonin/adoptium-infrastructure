#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Node.js contributors. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    from itertools import ifilter
except ImportError:
    from itertools import filter as ifilter
import json
import yaml
import os
import sys
from os import path


# customisation options per host:
#
# - ip [string] (required): ip address of host
# - alias [string]: 'nickname', will be used in ssh config
# - labels [sequence]: passed to jenkins
#
# parsing done on host naming:
#
# - *freebsd*: changes path to python interpreter
# - *smartos*: changes path to python interpreter
#
# @TODO: properly support --list and --host $host


def main():

    hosts = {}
    export = {'_meta': {'hostvars': {}}}

    # get inventory
    basepath = path.dirname(__file__)
    inventory_path = path.abspath(path.join(basepath, "..", "..", "inventory.yml"))
    with open(inventory_path, 'r') as stream:
        try:
            hosts = yaml.load(stream)

        except yaml.YAMLError as exc:
            print(exc)
        finally:
            stream.close()

    # get special cases
    config = configparser.ConfigParser()
    config.read('ansible.cfg')

    for host_types in hosts['hosts']:
        for host_type, providers in host_types.iteritems():
            export[host_type] = {}
            export[host_type]['hosts'] = []

            key = '~/.ssh/id_rsa'
            export[host_type]['vars'] = {
                'ansible_ssh_private_key_file': key
            }



    print(json.dumps(export, indent=2))


def parse_host(host):
    """Parses a host and validates it against our naming conventions"""

    hostinfo = dict()

    return hostinfo


def has_metadata(info):
    """Checks for metadata in variables. These are separated from the "key"
       metadata by underscore. Not used anywhere at the moment for anything
       other than descriptiveness"""

    param = dict()
    metadata = info.split('_', 1)

    try:
        key = metadata[0]
        metadata = metadata[1]
    except IndexError:
        metadata = False
        key = info

    return key if metadata else info




    main()
