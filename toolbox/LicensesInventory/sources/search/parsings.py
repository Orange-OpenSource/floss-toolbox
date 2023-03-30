#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import os
import json 
import xmltodict
from bs4 import BeautifulSoup
import bs4

from sources.common import CData


class CParsing:

    def __init__(self):
        self.ins_data = CData()

    def get_content(self, file):
        content = str()
        with open(file, 'rt', encoding='utf-8') as f:
            content = f.read()
        return content

    def clean(self, line):
        # keep only the text
        # even if there are images, links, etc
        html_code = '<html>'
        html_code += '<head>'
        html_code += '<meta charset=\"utf-8\">'
        html_code += '<title>titre</title>'
        html_code += '</head>'
        html_code += '<body>'

        line = line.strip()
        html_code += '<p>' + line + '</p>'

        html_code += '</body>'
        html_code += '</html>'

        soup = BeautifulSoup(html_code, 'html.parser')
        license = soup.p.get_text()

        return license

    def get_in_license(self, file):
        html_code = self.get_content(file)
        soup = BeautifulSoup(html_code, 'html.parser')

        for i in range(1, 10):
            my_head = 'h' + str(i)
            for head in soup.find_all(my_head):
                text = head.text.strip()
                if text == 'License':
                    r = head.find_all_next()
                    for v in r:
                        license = v.text.strip()
                        if license != str():
                            license = self.clean(license)
                            return [license]

        return [None]

    def get_license_for_flutter(self, file):
        result = list()

        content = self.get_content(file)
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
        license = content.strip()

        return [license]

    def get_license_for_go_github(self, file):
        result = list()

        content = self.get_content(file)
        p = content.find('License')
        content = content[p+1:]
        p = content.find('</svg>')
        content = content[p+1:]
        p = content.find('>')
        content = content[p+1:]
        p = content.find('<')
        content = content[0:p]
        license = content.strip()

        return [license]

    def get_license_for_go(self, file):
        result = list()

        content = self.get_content(file)
        p = content.find('license')
        content = content[p+1:]
        p = content.find('gtmc=')
        content = content[p+1:]
        p = content.find('>')
        content = content[p+1:]
        p = content.find('</a>')
        content = content[0:p]
        license = content.strip()

        return [license]

    def get_license_for_roast(self, file):
        result = list()

        content = self.get_content(file)
        p = content.find('license')
        content = content[p:]
        p = content.find('\"')
        content = content[p + 1:]
        p = content.find('\"')
        content = content[p + 1:]
        p = content.find('\"')
        content = content[:p]
        license = content.strip()

        return [license]

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
            license = data['items'][0]['license']['name']
            license = license.strip()
            the_data.append(license)
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
