#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

from ..common import CFile
from ..common import CFilter
from ..common import CData
from ..common import CName

class CParsing:
    """
    Helps to parse dependencies manager file
    """

    def __init__(self):
        self.head = '{'
        self.foot = '}'
        self.the_heads = list()
        self.the_foots = list()
        self.ins_data = CData()
        self.the_lines = list()

    def get_data(self, i, level):
        result = list()

        while i < len(self.the_lines):
            sub_found = self.the_lines[i] in self.the_heads
            if level > 1:
                sub_found = sub_found or self.head == self.the_lines[i][-1]
            if sub_found == True:
                level = level + 1
                i = i + 1
                r = self.get_data(i, level)
                temp, i = r
                result += temp
                level = level - 1
            elif level > 1:
                if self.the_lines[i] in self.the_foots:
                    return (result, i)
                else:
                    result.append(self.the_lines[i])
            i = i + 1

        return (result, i)

    def manage_gradle(self, the_lines):
        """
        To manage build.gradle and build.gradle.kts files
        """

        result = list()

        for line in the_lines:
            # head at the end
            if line[-1] == self.ins_data.head:
                continue

            # exclude
            if line.find('exclude') == 0:
                continue

            # the structure of the line
            start = 0

            ## quote before prefix
            quote_found = False
            if line[0] == self.ins_data.quote:
                quote_found = True
                start = start + 1

            ## first letter
            if line[start] not in self.ins_data.the_letters:
                continue

            ## prefix
            for i in range(start, len(line)):
                if line[i] not in self.ins_data.the_letters:
                    start = i + 0
                    break

            ## quote after prefix
            if line[start] == self.ins_data.quote and quote_found == True:
                # couple of quotes
                start = start + 1
            elif line[start] != self.ins_data.quote and quote_found == False:
                # no quote
                pass
            else:
                continue

            ## quote before the values
            the_values = line[start:]
            p_a = the_values.find(self.ins_data.quote)
            if p_a < 0 or p_a > 2:
                continue

            ## quote after the values
            the_values = the_values[p_a + 1:]
            p_b = line.find(self.ins_data.quote)
            if p_b < 0:
                continue

            # extract the values
            the_values = the_values.replace(self.ins_data.quote, '')
            the_fields = the_values.split(':')
            s = len(the_fields)
            namespace = ''
            component = ''
            if s == 3 or s == 2:
                namespace = the_fields[0]
                namespace = namespace.replace('.', '/')
                component = the_fields[1]
            else:
                component = the_fields[0]

            my_list = [component, namespace]
            result.append(my_list)

        return result

    def manage_package_json(self, the_lines):
        """
        To manage package.json files
        """
        result = list()

        separator = ':'
        for line in the_lines:
            the_fields = line.split(separator)
            if len(the_fields) != 2:
                continue

            # check the quotes
            component = the_fields[0]
            component = component.lstrip()
            component = component.rstrip()
            if component[0] != self.ins_data.quote or component[-1] != self.ins_data.quote:
                continue
            component = component.replace(self.ins_data.quote, '')
            #version = the_fields[1]
            my_list = [component]
            result.append(my_list)

        return result

    def get_data_for_each_block(self, the_lines):
        result = list()

        separator = ' = '
        head = '[[package]]'
        i = 0
        while i < len(the_lines):
            if the_lines[i].find(head) == 0:
                i += 1
                # search the line to threat
                while the_lines[i].find('name') != 0:
                    i += 1
                # threat
                the_fields = the_lines[i].split(separator)
                if len(the_fields) == 2:
                    # check the quotes
                    component = the_fields[1]
                    component = component.lstrip()
                    component = component.rstrip()
                    component = component.replace(self.ins_data.quote, '')
                    my_list = [component]
                    result.append(my_list)

            i += 1

        return result

    def check_allowed_characters_in_string(self, my_string, the_allowed_characters):
        number_found = True

        for c in my_string:
            if c not in the_allowed_characters:
                number_found = False
                break

        return number_found

    def get_data_for_flutter(self, the_lines):
        """
        To manage pubspec.yaml files
        """
        result = list()

        the_allowed_characters = list()
        for v in range(0, 10):
            the_allowed_characters.append(str(v))
        separator = ':'
        i = 0
        block_found = False
        for line in the_lines:
            if line in self.the_heads:
                block_found = True
                continue
            if block_found == True and line == str():
                block_found = False
                continue

            if block_found == True:
                the_fields = line.split(separator)
                if len(the_fields ) == 1:
                    continue
                if the_fields[1] == str():
                    continue

                component = the_fields[0]
                # version
                version = the_fields[1]
                version = version.replace('^', str())
                version = version.replace(' ', str())
                the_fields = version.split('.')
                value = the_fields[0]
                if value == str():
                    continue
                if self.check_allowed_characters_in_string(value, the_allowed_characters) == False:
                    continue

                p = component.find('(')
                if p > -1:
                    component = component[0:p]
                component = component.strip()
                my_list = [component]
                result.append(my_list)

        return result

    def manage_go(self, the_lines):
        """
        To manage go.mod files
        """
        result = list()

        for line in the_lines:
            new_line = line.replace(' ', '')
            if '//indirect' in new_line:
                continue
            new_line = line.lstrip()
            the_fields = new_line.split(' ')
            component = the_fields[0]
            my_list = [component]
            result.append(my_list)

        return result

    def manage_swift(self, the_lines):
        """
        To manage Package.swift files
        """
        result = list()

        for line in the_lines:
            p = line.find('.package')
            if p != 0:
                continue
            p = line.find('https://github.com/')
            if p < 0:
                continue

            line = line[p:]
            p = line.find('\"')
            line = line[:p]
            component = line.strip()
            my_list = [component]
            result.append(my_list)

        return result

    def get_the_values(self, language, the_lines, ins_filter):
        result = list()

        self.the_lines = the_lines
        ins_name = CName()

        if language == ins_name.gradle:
            r = self.get_data(0, 1)
            the_lines, i = r
            result = self.manage_gradle(the_lines)
        elif language == ins_name.package_json:
            r = self.get_data(0, 1)
            the_lines, i = r
            result = self.manage_package_json(the_lines)
        elif language == ins_name.roast:
            result = self.get_data_for_each_block(the_lines)
        elif language == ins_name.go:
            r = self.get_data(0, 1)
            the_lines, i = r
            result = self.manage_go(the_lines)
        elif language == ins_name.flutter:
            result = self.get_data_for_flutter(the_lines)
        elif language == ins_name.swift:
            r = self.get_data(0, 1)
            the_lines, i = r
            result = self.manage_swift(the_lines)

        return result
