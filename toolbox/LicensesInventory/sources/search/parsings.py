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
import html
from sources.common import CData

space = ' '

class CParsing:

    def __init__(self):
        self.ins_data = CData()

    def get_content(self, file):
        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()
        #content = content.replace('\n', str())
        content = html.unescape(content)
        return content

    def b_get_license_with_html(self, file):
        result = list()

        html_code = self.get_content(file)
        soup = BeautifulSoup(html_code, 'html.parser')

        the_a = soup.find_all()

    def get_license_with_html(self, file):
        result = list()

        html_code = self.get_content(file)
        soup = BeautifulSoup(html_code, 'html.parser')

        i = 1
        while i < 11:
            v = 'h' + str(i)
            the_heads = soup.find_all(v)
            for head in the_heads:
                if 'license' not in head.get_text().lower(): continue
                the_siblings = head.next_siblings
                for sibling in the_siblings:
                    if type(sibling) == bs4.element.Tag:
                        return [sibling.get_text().strip()]

            i += 1

        return result

    def get_license_for_go(self, file):
        the_values_for_license = list()

        content = self.get_content(file)
        p = content.find('license')
        if p < 0: return the_values_for_license
        content = content[p+1:]
        p = content.find('gtmc=')
        if p < 0: return the_values_for_license
        content = content[p+1:]
        p = content.find('>')
        if p < 0: return the_values_for_license
        content = content[p+1:]
        p = content.find('</a>')
        if p < 0: return the_values_for_license
        content = content[0:p]
        text = content.strip()
        the_values_for_license.append(text)

        return the_values_for_license

    def get_license_for_roast(self, file):
        the_values_for_license = list()

        content = self.get_content(file)
        p = content.find('license')
        if p < 0: return the_values_for_license
        content = content[p:]
        p = content.find('\"')
        if p < 0: return the_values_for_license
        content = content[p + 1:]
        p = content.find('\"')
        if p < 0: return the_values_for_license
        content = content[p + 1:]
        p = content.find('\"')
        if p < 0: return the_values_for_license
        content = content[:p]
        text = content.strip()
        the_values_for_license.append(text)

        return the_values_for_license

    def get_license_for_github(self, file):
        result = list()

        data = None
        try:
            with open(file, encoding='utf-8') as f: 
                data = f.readlines()
        except Exception as e:
            print('Error: reading the content of the downloaded file to json.\n\t' + file)
            return result

        try:
            #convert to json
            line = str()
            if len(data) == 1:
                line = data[0]
            else:
                for v in data:
                    line += v
            data = json.loads(line)
        except Exception as e:
            print('Error: converting the content of the downloaded file to json.')
            return result

            if data['total_count' ] > 500000:
                return result

        component = str()
        try:
            component = data['items'][0]['name']
            component = component.strip()
        except Exception as e:
            component = str()

        license = str()
        try:
            license = data['items'][0]['license']['name']
            license = license.strip()
        except Exception as e:
            license = str()

        result.append(component)
        result.append(license)
        return result

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

