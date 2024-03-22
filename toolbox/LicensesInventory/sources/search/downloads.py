#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license,
# the text of which is available at https://opensource.org/license/apache-2-0
# or see the "LICENSE.txt" file for more details.
#
# Authors: See CONTRIBUTORS.txt
# Software description: A toolbox of scripts to help work of forges admins and open source referents

import time
import os
import requests

from sources.common import CFile, CName, CDateFromRetryAfter


class CDownload:

    def __init__(self):
        self.ins_file = CFile()
        self.ins_filter = None
        self.ins_name = CName()
        self.path_licenses = str()
        self.error_code = None
        self.sleep = 2.5
        self.the_letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@_')
        self.next_date = None

    def rename(self, filename):
        result = str()

        for i in range(0, len(filename)):
            c = filename[i]
            if c not in self.the_letters:
                c = '_'
            result += c

        return result

    def get_data(self, platform, the_key_and_dependency, namespace):
        result = list()

        # models
        url = self.ins_filter.the_URLs[platform]
        filename = self.ins_filter.the_filenames[platform]

        # from main
        component = the_key_and_dependency['component']

        # url
        if platform == self.ins_name.go_github:
            url = 'https://' + component
        elif platform == self.ins_name.swift:
            url = component
        else:
            for key, parameter in the_key_and_dependency.items():
                url = url.replace('[' + key + ']', parameter)

        # file
        if platform == self.ins_name.swift:
            component = component.replace('https://github.com/', str())
        elif platform == self.ins_name.gradle:
            if namespace != None:
                filename = filename.replace('[component]', component + '__' + namespace)

        filename = filename.replace('[component]', component)

        before = str()
        extension = str()
        for i in range(len(filename) -1, -1, -1):
            if filename[i] == '.':
                before = filename[:i]
                extension = filename[i:]
                break

        before = self.rename(before)
        filename = before + extension

        return [url, filename, component]

    def manage_status(self, component, response):
        code = int(response.status_code)
        self.error_code = str(code)

        if code < 300: return

        msg = 'INFO: ' + component + ': '
        msg += 'status-code=' + str(code)
        print(msg)

        try:
            my_date_time = response.retry_after
            r = CDateFromRetryAfter().get(my_date_time)
            next_date, delay = r
            self.next_date = next_date
            self.delay = delay
        except Exception as e:
            self.next_date = None

        raise Exception()

    def write_in_file(self, response, filename):
        content = response.text
        the_lines = content.split('\n')

        if os.path.isdir(self.path_licenses) == False:
            os.mkdir(self.path_licenses)
        file = None
        try:
            self.ins_file.write_in_text_file(self.path_licenses, filename, the_lines)
            file = os.path.join(self.path_licenses, filename)
        except Exception as e:
            raise Exception(e.__str__())

        return file

    def manage_sleep(self, platform, interval):
        the_platforms = [self.ins_name.package_json]
        if platform in the_platforms:
            to_wait = self.sleep - interval
            if to_wait > 0:
                time.sleep(to_wait)

    def get_file(self, platform, the_key_and_dependency, namespace):
        result = None

        r = self.get_data(platform, the_key_and_dependency, namespace)
        url = r[0]
        filename = r[1]
        component = r[2]

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        response = None
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers)
            interval = time.time() - start_time
            self.manage_sleep(platform, interval)
            self.manage_status(component, response)
            result = self.write_in_file(response, filename)
        except requests.exceptions.RequestException as e:
            self.manage_status(component, response)
        except Exception as e:
            #print(e.__str__())
            return None

        return result
