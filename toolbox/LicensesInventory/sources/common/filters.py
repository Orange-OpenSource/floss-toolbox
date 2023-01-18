#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from .names import CName
from .datas import CData
from .files import CFile


class CFilter:

    def __init__(self):
        self.ins_name = CName()
        self.ins_data = CData()
        self.ins_config = None
        self.the_contents = dict()
        self.the_heads = dict()
        self.the_foots = dict()
        self.the_URLs = dict()
        self.the_filenames = dict()
        self.the_commands = dict()

    def get_content_by_name(self, ins_name):
        print('\t➡️  Getting content by name...')
        result = dict()

        ins_file = CFile()
        the_files = ins_file.get_the_files(self.ins_config.path_dependencies, self.ins_config.the_filenames)

        if len(the_files) == 0:
            raise Exception('\t💥  Unable to go further, missing data (files for the filter) to process.')

        content_gradle = list()
        content_package_json = list()
        content_roast = list()
        content_go = list()
        content_flutter = list()
        content_swift = list()

        for file in the_files:
            the_fields = os.path.split(file)
            path = the_fields[0]
            filename = the_fields[1]
            if ins_name.gradle in filename:
                content_gradle += ins_file.read_text_file (path, filename)
            elif ins_name.package_json == filename:
                content_package_json += ins_file.read_text_file (path, filename)
            elif ins_name.roast == filename:
                content_roast += ins_file.read_text_file (path, filename)
            elif ins_name.go == filename:    
                content_go += ins_file.read_text_file (path, filename)
            elif ins_name.flutter == filename:    
                content_flutter += ins_file.read_text_file (path, filename)
            elif ins_name.swift == filename:    
                content_swift += ins_file.read_text_file (path, filename)

        if len(content_gradle) > 0:
            result[ins_name.gradle] = content_gradle
        if len(content_package_json) > 0:
            result[ins_name.package_json] = content_package_json
        if len(content_roast) > 0:
            result[ins_name.roast] = content_roast
        if len(content_go) > 0:
            result[ins_name.go] = content_go
        if len(content_flutter) > 0:
            result[ins_name.flutter] = content_flutter
        if len(content_swift) > 0:
            result[ins_name.swift] = content_swift

        print('\t\t✅ Getting content by name... OK!')
        return result

    def get_the_heads_by_name(self, ins_name):
        print('\t➡️  Getting the heads by name...')
        result = dict()

        result[ins_name.gradle] = ['dependencies {']

        quote = self.ins_data.quote
        h_a = quote + 'peerDependencies' + quote + ': {'
        h_b = quote + 'devDependencies' + quote + ': {'
        h_c = quote + 'dependencies' + quote + ': {'
        h_d = '{'
        result[ins_name.package_json] = [h_a, h_b, h_c]

        result[ins_name.roast] = ['[[package]]']
        result[ins_name.go] = ['require (']
        result[ins_name.flutter] = ['dependencies:', 'dev_dependencies:']
        result[ins_name.swift] = ['dependencies: [']

        print('\t\t✅ Getting the heads by name... OK!')
        return result

    def get_the_foots_by_name(self, ins_name):
        print('\t➡️  Getting the foots by name...')
        result = dict()

        foot = '}'
        comma = ','
        result[ins_name.gradle] = [foot, foot + comma]
        result[ins_name.package_json] = [foot, foot + comma]
        result[ins_name.roast] = [str()]
        result[ins_name.go] = [')']
        result[ins_name.flutter] = [str()]
        result[ins_name.swift] = [']', '],']

        print('\t\t✅ Getting the foots by name... OK!')
        return result

    def get_the_URLs_by_name(self, ins_name):
        print('\t➡️  Getting the URLs by name...')
        result = dict()

        # maven central
        result[ins_name.version_for_maven_central] = "https://search.maven.org/solrsearch/select?q=g:[namespace]%20AND%20a:[component]"
        result[ins_name.maven_central] = "https://search.maven.org/remotecontent?filepath=[namespace]/[component]/[version]/[component]-[version].pom"
        result[ins_name.github] = "https://api.github.com/search/repositories?q=[component]"

        # the others
        result[ins_name.package_json] = "https://www.npmjs.com/package/[component]"
        result[ins_name.roast] = 'https://crates.io/api/v1/crates/[component]'
        result[ins_name.go] = 'https://pkg.go.dev/[component]'
        result[ins_name.go_github] = 'https://github.com/[component]'
        result[ins_name.flutter] = 'https://pub.dev/packages/[component]'
        result[ins_name.swift] = str()

        print('\t\t✅ Getting the URLs by name... OK!')
        return result

    def get_the_filenames_by_name(self, ins_name):
        print('\t➡️  Getting the filenames by name...')
        result = dict()

        # maven central
        result[ins_name.maven_central] = '[component]_maven_central.pom'
        result[ins_name.version_for_maven_central] = 'version_[component].json'
        result[ins_name.github] = '[component]_github.json'

        # the others
        result[ins_name.package_json] = '[component].html'
        result[ins_name.roast] = '[component].json'
        result[ins_name.go] = '[component].html'
        result[ins_name.go_github] = '[component].html'
        result[ins_name.flutter] = '[component].html'
        result[ins_name.swift] = '[component].html'

        print('\t\t✅ Getting the filenames by name... OK!')
        return result

    def manage_the_comments(self, the_lines, i):
        line = the_lines[i]
        line = line.strip()

        # invalid line
        if len(line) < 2:
            return -1

        # simple comment
        my_string = line[0:1]
        if my_string == '#':
            return i

        my_string = line[0:2]
        if my_string == self.ins_data.the_comments[0]:
            return i

        # complex comment
        if my_string == self.ins_data.the_comments[1]:
            while self.ins_data.the_comments[2] not in the_lines[i]:
                i += 1
            return i

        return -1

    def delete_the_comments(self, the_lines):
        print('\t➡️  Deleting the comments...')
        result = list()

        i = 0
        while i < len(the_lines):
            j = self.manage_the_comments(the_lines, i)
            if j == -1:
                result.append(the_lines[i])
            else:
                i = j + 0
            i += 1

        print('\t\t✅ Deleting the comments... OK!')
        return result

    def clean(self, the_lines, platform):
        print('\t➡️  Cleaning...')
        result = list()

        for line in the_lines:
            line = line.lstrip()
            line = line.rstrip()
            if platform != self.ins_name.roast and platform != self.ins_name.flutter:
                if line == str():
                    continue
            line = line.replace(self.ins_data.old_quote, self.ins_data.quote)
            result.append(line)

        print('\t\t✅ Cleaning... OK!')
        return result

    def prepare(self, ins_config):
        print('\t➡️  Preparing CFilter...')
        self.ins_config = ins_config

        # to get the data
        self.the_heads = self.get_the_heads_by_name(self.ins_name)
        self.the_foots = self.get_the_foots_by_name(self.ins_name)

        # to download the licenses
        self.the_URLs = self.get_the_URLs_by_name(self.ins_name)
        self.the_filenames = self.get_the_filenames_by_name(self.ins_name)

        # others
        self.the_contents = self.get_content_by_name(self.ins_name)
        print('\t\t✅ Preparing CFilter... OK!')

    def filter(self, the_lines, platform):
        result = list()

        the_lines = self.delete_the_comments(the_lines)
        result = self.clean(the_lines, platform)

        return result
