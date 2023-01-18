#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import sys
import time
import os
import json 
import xmltodict

from sources.common import CData

class CParsing:
    """
    Helps to parse some files extracted from online forges or platforms.
    Manages some environements like Swift, Flutter, Go, Rust, JS, GitHub and Maven Central.
    Strong relationship between platforms outputs (like github.com, npmjs.org, maven central...) and that class.
    """

    def __init__(self):
        self.ins_data = CData()

    def get_license_for_swift(self, file):
        result = list()

        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()

        p = content.find('License')
        if p < 0: return [None]
        content = content[p+1:]
        value = '</svg>'
        p = content.find(value)
        if p < 0: return [None]
        content = content[p+len(value):]
        p = content.find('<')
        if p < 0: return [None]
        content = content[:p]
        content = content.strip()

        return [content]

    def get_license_for_flutter(self, file):
        result = list()

        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()

        p = content.find('License</h3')
        content = content[p+1:]
        p = content.find('LICENSE')
        content = content[0:p]

        p = content.find('height=')
        content = content[p+1:]
        p = content.find('>')
        content = content[p+1:]
        p = content.find('(')
        content = content[:p]
        content = content.strip()

        return [content]

    def get_license_for_go_github(self, file):
        result = list()

        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()

        p = content.find('License')
        content = content[p+1:]
        p = content.find('</svg>')
        content = content[p+1:]
        p = content.find('>')
        content = content[p+1:]
        p = content.find('<')
        content = content[0:p]
        content = content.strip()

        return [content]

    def get_license_for_go(self, file):
        result = list()

        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()

        p = content.find('license')
        content = content[p+1:]
        p = content.find('gtmc=')
        content = content[p+1:]
        p = content.find('>')
        content = content[p+1:]
        p = content.find('</a>')
        content = content[0:p]
        content = content.strip()

        return [content]

    def get_license_for_roast(self, file):
        result = list()

        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()

        p = content.find('license')
        content = content[p:]
        p = content.find('\"')
        content = content[p + 1:]
        p = content.find('\"')
        content = content[p + 1:]
        p = content.find('\"')
        content = content[:p]

        return [content]

    def get_license_for_package_json(self, file):
        result = list()

        the_lines = list()
        with open(file, 'rt', encoding='utf-8') as f:
            the_lines = f.readlines()

        i = 0
        while i < len(the_lines):
            line = the_lines[i]
            if 'version' in line:
                if 'License' in line:
                    p = line.find('License')
                    line = line[p:]
                    p = line.find('<p')
                    line = line[p:]
                    p = line.find('>')
                    line = line[p + 1:]
                    p = line.find('<')
                    license = line[:p]
                    result.append(license)
            i += 1

        return result

    def get_license_for_github(self, file):
        the_data = list()

        data = None
        try:
            with open(file) as f: 
                data = json.load(f)

            total = 'total_count'
            if 500000 < data[total]:
                return None

            # component
            the_data.append(data['items'][0]['name'])
            # license
            the_data.append(data['items'][0]['license']['name'])
        except Exception as e:
            return None

        return the_data

    def get_license_for_maven_central(self, file):
        result = list()

        my_xml = None
        my_dict = None
        try:
            with open(file, 'r', encoding='utf-8') as file:
                my_xml = file.read()
            my_dict = xmltodict.parse(my_xml)

            # component
            result.append(my_dict['project']['name'])
            # license
            result.append(my_dict['project']['licenses']['license']['name'])
        except Exception:
            return None

        return result

    def extract_version_for_maven_central(self, file):
        version = str()

        data = None
        try:
            with open(file) as f: 
                data = json.load(f)

            if int(data['response']['numFound']) < 1:
                return None

            version = data['response']['docs'][0]['latestVersion']
        except Exception:
            return None

        return version
