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

import json 
import xmltodict
from bs4 import BeautifulSoup
import bs4

from sources.common import CData

space = ' '

class CParsing:

    def __init__(self):
        self.ins_data = CData()

    def get_content(self, file):
        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()
        return content

    def get_license_with_html(self, file):
        result = None

        html_code = self.get_content(file)
        soup = BeautifulSoup(html_code, 'html.parser')

        text = str()
        for i in range(1, 10):
            my_head = 'h' + str(i)
            for head in soup.find_all(my_head):
                if 'license' not in head.text.lower(): continue

                license = head.next_sibling
                while type(license) != bs4.element.Tag:
                    license = license.next_sibling

                first_found = False
                if text == str():
                    first_found = True
                tmp = license.text
                tmp = tmp.replace('\n', str())
                tmp = tmp.strip()
                if first_found == True:
                    text = tmp
                else:
                    my_tmp = tmp.lower()
                    my_text = text.lower()
                    if (my_tmp != my_text) and(my_tmp not in my_text):
                        text = text + ' ' + tmp

        if text == str(): text = None
        return [text]

    def get_license_for_go_github(self, file):
        result = list()

        content = self.get_content(file)
        p = content.find('License')
        if p < 0: return None
        content = content[p+1:]
        p = content.find('</svg>')
        if p < 0: return None
        content = content[p+1:]
        p = content.find('>')
        if p < 0: return None
        content = content[p+1:]
        p = content.find('<')
        if p < 0: return None
        content = content[0:p]
        license = content.strip()

        return [license]

    def get_license_for_go(self, file):
        result = list()

        content = self.get_content(file)
        p = content.find('license')
        if p < 0: return None
        content = content[p+1:]
        p = content.find('gtmc=')
        if p < 0: return None
        content = content[p+1:]
        p = content.find('>')
        if p < 0: return None
        content = content[p+1:]
        p = content.find('</a>')
        if p < 0: return None
        content = content[0:p]
        license = content.strip()

        return [license]

    def get_license_for_roast(self, file):
        result = list()

        content = self.get_content(file)
        p = content.find('license')
        if p < 0: return None
        content = content[p:]
        p = content.find('\"')
        if p < 0: return None
        content = content[p + 1:]
        p = content.find('\"')
        if p < 0: return None
        content = content[p + 1:]
        p = content.find('\"')
        if p < 0: return None
        content = content[:p]
        license = content.strip()

        return [license]

    def get_license_for_github(self, file):
        the_data = list()

        data = None
        try:
            with open(file, encoding='utf-8') as f: 
                data = f.readlines()

            #convert to json
            line = str()
            if len(data) == 1:
                line = data[0]
            else:
                for v in data:
                    line += v
            data = json.loads(line)

        except Exception as e:
            print('💥  Error: converting the content of the downloaded file to json.')
            return None

            if data['total_count' ] > 500000:
                return None

        try:
            component = data['items'][0]['name']
            component = component.strip()
        except Exception as e:
            component = 'None'

        try:
            license = data['items'][0]['license']['name']
            license = license.strip()
        except Exception as e:
            license = 'None'

        the_data = [component, license]
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
            license = my_dict['project']['licenses']['license']['name']
            license = license.strip()
            result.append(license)
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
            version = version.strip()
        except Exception:
            return None

        return version

