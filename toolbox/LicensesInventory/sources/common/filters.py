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

import os

from .names import CName
from .datas import CData
from .files import CFile
from .comments import CComment
from .data_in_blocks import CDataInBlock

class CFilter:

    def __init__(self):
        self.ins_name = CName()
        self.ins_data = CData()
        self.ins_config = None

        self.the_heads = dict()
        self.the_foot = dict()
        self.the_URLs = dict()
        self.the_filenames = dict()
        self.the_commands = dict()
        self.the_contents = dict()
        self.the_platform_to_treat = list()
        self.the_contents_on_error = dict()

    def get_content_by_name(self, ins_name):
        result = dict()

        for filename in self.ins_config.the_filenames:
            platform = self.get_platform(filename)
            self.the_platform_to_treat.append(platform)

        path = self.ins_config.path_dependencies
        if os.path.isdir(path) == False:
            print('No path to extract the dependencies.')
            return dict()

        the_files = list()
        for filename in self.ins_config.the_filenames:
            the_files += CFile().get_the_files_by_names(self.ins_config.path_dependencies, filename)
        if len(the_files) == 0:
            msg = 'No file to extract the dependencies.'
            print(msg)
            return dict()

        # extract the contents
        for file in the_files:
            the_fields = os.path.split(file)
            path = the_fields[0]
            filename = the_fields[1]
            platform = self.get_platform(filename)

            the_lines = CFile().read_text_file (path, filename)
            the_lines = self.clean(the_lines, platform)

            s = len(the_lines)
            if s == 0:
                continue

            data_found = False
            for line in the_lines:
                if line != str():
                    data_found = True
                    break

            if data_found == True:
                if platform in result.keys():
                    result[platform] += the_lines
                else:
                    result[platform] = the_lines

        return result

    def get_content_on_error_by_platform(self):
        result = dict()

        path_errors = self.ins_config.path_errors
        if os.path.isdir(path_errors) == False:
            print('No path to extract the dependencies on error.')
            return dict()

        the_platform = self.the_platform_to_treat
        if len(self.the_platform_to_treat) == 0:
            the_platform = CName().get_the_platforms()
        for platform in the_platform:
            try:
                filename_errors = self.ins_config.model_for_errors_file.replace('[platform]', platform)
                the_lines = CFile().read_text_file (path_errors, filename_errors)
                the_lines = self.clean(the_lines, platform)
                result[platform] = the_lines
            except Exception as e:
                pass

        return result

    def get_platform(self, filename):
            if self.ins_name.gradle.lower() in filename.lower():
                return self.ins_name.gradle
            if self.ins_name.package_json.lower() == filename.lower():
                return self.ins_name.package_json
            if self.ins_name.roast.lower() == filename.lower():
                return self.ins_name.roast
            if self.ins_name.go.lower() == filename.lower():
                return self.ins_name.go
            if self.ins_name.flutter.lower() == filename.lower():
                return self.ins_name.flutter
            if self.ins_name.swift.lower() == filename.lower():
                return self.ins_name.swift
            if self.ins_name.cocoapods.lower() == filename.lower():
                return self.ins_name.cocoapods

    def get_the_heads_by_name(self, ins_name):
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
        result[ins_name.cocoapods] = None

        quote = '\"'
        a = quote + 'dependencies' + quote + ': {'
        b = quote + 'test-dependencies' + quote + ': {'
        c = quote + 'dev-dependencies' + quote + ': {'
        #result[ins_name.elm_lang] = [a, b, c]

        return result

    def get_the_foot_by_name(self, ins_name):
        result = dict()

        feet = '}'
        comma = ','
        result[ins_name.gradle] = [feet, feet + comma]
        result[ins_name.package_json] = [feet, feet + comma]
        result[ins_name.roast] = [str()]
        result[ins_name.go] = [')']
        result[ins_name.flutter] = [str()]
        result[ins_name.swift] = [']', '],']
        result[ins_name.cocoapods] = None
        #result[ins_name.elm_lang] = [foot, foot + comma]

        return result

    def get_the_URLs_by_name(self, ins_name):
        result = dict()

        # gradle
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
        result[ins_name.cocoapods] = 'https://cocoapods.org/pods/[component]'
        #result[ins_name.elm_lang] = 'https://package.elm-lang.org/packages/[component]/latest/about'

        return result

    def get_the_filenames_by_name(self, ins_name):
        result = dict()

        # gradle
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
        result[ins_name.cocoapods] = '[component].html'
        #result[ins_name.elm_lang] = '[component].html'

        return result

    def clean(self, the_lines, platform):
        result = list()

        for line in the_lines:
            my_line = line.replace(self.ins_data.old_quote, self.ins_data.quote)
            result.append(my_line)

        result = CComment().delete(result)

        return result

    def get_the_data(self, the_lines_by_platform):
        result = dict()

        for platform, the_lines in the_lines_by_platform.items():
            if platform == self.ins_name.cocoapods:
                result[platform] = the_lines
                continue

            heads = self.the_heads[platform]
            foot = self.the_foot[platform]
            ends_with_feet = False
            if (platform == self.ins_name.flutter) or (platform == self.ins_name.roast):
                ends_with_feet = True
            data_with_head = False
            if platform == CName().gradle:
                data_with_head = True
            the_new_lines = CDataInBlock(heads, foot).get(the_lines, ends_with_feet, data_with_head)
            result[platform] = the_new_lines

        return result

    def prepare(self, ins_config):
        self.ins_config = ins_config

        # data in ini file
        if ins_config.path_licenses == str():
            raise Exception('The path to store the licenses is not precised in the ini file.')
        if os.path.isdir(ins_config.path_licenses) == False:
            raise Exception('The path to store the licenses does not exist.')

        try:
            ins_config.number_of_errors_max = int(ins_config.number_of_errors_max)
        except Exception as e:
            raise Exception('The number of authorized errors is not valid in the ini file.')

        # to get the data
        self.the_heads = self.get_the_heads_by_name(self.ins_name)
        self.the_foot = self.get_the_foot_by_name(self.ins_name)

        # to download the licenses
        self.the_URLs = self.get_the_URLs_by_name(self.ins_name)
        self.the_filenames = self.get_the_filenames_by_name(self.ins_name)

        # others
        the_content_by_platform = self.get_content_by_name(self.ins_name)
        the_content_on_error_by_platform = self.get_content_on_error_by_platform()

        self.the_contents = self.get_the_data(the_content_by_platform)
        self.the_contents_on_error = the_content_on_error_by_platform
