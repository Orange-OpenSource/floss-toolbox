#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import time
import os
import requests

from sources.common import CName

class CDownload:
    """
    Helps to download useful files from platforms to parse them later
    """

    def __init__(self):
        self.ins_filter = None
        self.ins_name = CName()
        self.path_licenses = str()
        self.timeout = 20

    def get_data(self, platform, the_key_and_dependency):
        
        print('\t➡️  Getting data for platform ', platform, "...")
        result = list()

        # models
        url = self.ins_filter.the_URLs[platform]
        filename = self.ins_filter.the_filenames[platform]

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
        file = os.path.join(self.path_licenses, filename)

        print('\t\t✅ Getting data for platform ', platform, "... OK!")
        return [url, file]

    def get_file(self, platform, the_key_and_dependency, result, indice):

        r = self.get_data(platform, the_key_and_dependency)
        url = r[0]
        file = r[1]

        print('\t➡️  Getting file for platform ', platform, 'at URL ', url, "...")
        try:
            req = requests.get(url)
            if req.status_code >= 300:
                return None
            content = req.text.encode('utf-8')
            content = content.decode('ascii', 'ignore')
            the_lines = content.split('\n')
            with open(file, 'wt', encoding='utf-8') as f:
                for line in the_lines:
                    f.write(line)
            result.insert(indice, file)
        except Exception:
            return None

        print("\t\t✅ Getting file for platform ... OK!")
        return result
