#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

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
        result = dict()

        ins_file = CFile()
        the_files = ins_file.get_the_files(self.ins_config.path_dependencies, self.ins_config.the_filenames)

        content_gradle = list()
        content_package_json = list()
        content_roast = list()
        content_go = list()
        content_flutter = list()
        content_swift = list()
        content_cocoapods = list()
        content_elm_lang = list()

        for file in the_files:
            the_fields = os.path.split(file)
            path = the_fields[0]
            filename = the_fields[1]
            if ins_name.gradle.lower() in filename.lower():
                content_gradle += ins_file.read_text_file (path, filename)
            elif ins_name.package_json.lower() == filename.lower():
                content_package_json += ins_file.read_text_file (path, filename)
            elif ins_name.roast.lower() == filename.lower():
                content_roast += ins_file.read_text_file (path, filename)
            elif ins_name.go.lower() == filename.lower():
                content_go += ins_file.read_text_file (path, filename)
            elif ins_name.flutter.lower() == filename.lower():
                content_flutter += ins_file.read_text_file (path, filename)
            elif ins_name.swift.lower() == filename.lower():
                content_swift += ins_file.read_text_file (path, filename)
            elif ins_name.cocoapods.lower() == filename.lower():    
                content_cocoapods += ins_file.read_text_file (path, filename)
            elif ins_name.elm_lang.lower() == filename.lower():    
                content_elm_lang += ins_file.read_text_file (path, filename)

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
        if len(content_cocoapods) > 0:
            result[ins_name.cocoapods] = content_cocoapods
        if len(content_elm_lang) > 0:
            result[ins_name.elm_lang] = content_elm_lang

        return result

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

        #elm_lang
        quote = '\"'
        a = quote + 'dependencies' + quote + ': {'
        b = quote + 'test-dependencies' + quote + ': {'
        c = quote + 'dev-dependencies' + quote + ': {'
        result[ins_name.elm_lang] = [a, b, c]

        return result

    def get_the_foots_by_name(self, ins_name):
        result = dict()

        foot = '}'
        comma = ','
        result[ins_name.gradle] = [foot, foot + comma]
        result[ins_name.package_json] = [foot, foot + comma]
        result[ins_name.roast] = [str()]
        result[ins_name.go] = [')']
        result[ins_name.flutter] = [str()]
        result[ins_name.swift] = [']', '],']
        result[ins_name.cocoapods] = None
        result[ins_name.elm_lang] = [foot, foot + comma]

        return result

    def get_the_URLs_by_name(self, ins_name):
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
        result[ins_name.cocoapods] = 'https://cocoapods.org/pods/[component]'
        result[ins_name.elm_lang] = 'https://package.elm-lang.org/packages/[component]/latest/about'

        return result

    def get_the_filenames_by_name(self, ins_name):
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
        result[ins_name.cocoapods] = '[component].html'
        result[ins_name.elm_lang] = '[component].html'

        return result

    def manage_the_comments(self, the_lines, i):
        line = the_lines[i]
        line = line.strip()

        # simple comment
        if len(line) == 0:
            return -1
        if line[0] == '#':
            return i

        if len(line) < 2:
            return -1
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
        result = list()

        i = 0
        while i < len(the_lines):
            j = self.manage_the_comments(the_lines, i)
            if j == -1:
                result.append(the_lines[i])
            else:
                i = j + 0
            i += 1

        return result

    def clean(self, the_lines, platform):
        result = list()

        for line in the_lines:
            if platform != self.ins_name.flutter:
                line = line.strip()
            if platform != self.ins_name.roast and platform != self.ins_name.flutter:
                if line == str():
                    continue
            line = line.replace(self.ins_data.old_quote, self.ins_data.quote)
            result.append(line)

        return result

    def prepare(self, ins_config):
        self.ins_config = ins_config

        # to get the data
        self.the_heads = self.get_the_heads_by_name(self.ins_name)
        self.the_foots = self.get_the_foots_by_name(self.ins_name)

        # to download the licenses
        self.the_URLs = self.get_the_URLs_by_name(self.ins_name)
        self.the_filenames = self.get_the_filenames_by_name(self.ins_name)

        # others
        self.the_contents = self.get_content_by_name(self.ins_name)

    def filter(self, the_lines, platform):
        result = list()

        the_lines = self.clean(the_lines, platform)
        result = self.delete_the_comments(the_lines)

        return result
