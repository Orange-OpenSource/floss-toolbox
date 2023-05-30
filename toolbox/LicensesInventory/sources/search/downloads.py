#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import time
import os
import requests

from sources.common import CFile, CName

class CDownload:

    def __init__(self):
        self.ins_file = CFile()
        self.ins_filter = None
        self.ins_name = CName()
        self.path_licenses = str()
        self.error_code = None
        self.sleep = 2.5

    def get_data(self, platform, the_key_and_dependency):
        print('\t➡️  Getting data for platform ', platform, "...")
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
        filename = filename.replace('[component]', component)
        extension = str()
        for i in range(len(filename) -1, -1, -1):
            if filename[i] == '.':
                extension = filename[i:]
                break
        filename = filename.replace(extension, str())
        new_filename = filename
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        for c in filename:
            if c not in allowed_chars:
                new_filename = new_filename.replace(c, '_')
        filename = new_filename + extension

        return [url, filename, component]

    def manage_status(self, component, response):
        code = int(response.status_code)
        msg = component + ': '
        msg += 'status-code=' + str(code)
        self.error_code = str(code)

        if code > 299:
            print(msg)

    def write_in_file(self, response, filename):
        content = response.text
        the_lines = content.split('\n')

        self.ins_file.write_in_text_file(self.path_licenses, filename, the_lines)
        file = os.path.join(self.path_licenses, filename)

        return file

    def manage_sleep(self, platform, interval):
        the_platforms = [self.ins_name.package_json]
        if platform in the_platforms:
            to_wait = self.sleep - interval
            if to_wait > 0:
                time.sleep(to_wait)

    def get_file(self, platform, the_key_and_dependency):
        print('\t➡️  Getting file for platform ', platform, '...')
        result = None

        r = self.get_data(platform, the_key_and_dependency)
        url = r[0]
        filename = r[1]
        component = r[2]

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        try:
            start_time = time.time()
            response = requests.get(url, headers=headers)
            interval = time.time() - start_time
            self.manage_sleep(platform, interval)
            self.manage_status(component, response)
            result = self.write_in_file(response, filename)
        except Exception as e:
            return None

        return result
