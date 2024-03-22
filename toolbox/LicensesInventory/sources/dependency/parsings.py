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

from ..common import CData, CDataInBlock
from ..common import CName


class CParsing:

    def __init__(self):
        self.head = '{'
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
        result = list()

        for tmp in the_lines:
            line = tmp.strip()
            if line == str(): continue
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
            p = the_values.find('//')
            if p > -1:
                the_values = the_values[:p]
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
        result = list()

        separator = ':'
        for line in the_lines:
            the_fields = line.split(separator)
            if len(the_fields) != 2:
                continue

            # check the quotes
            component = the_fields[0]
            component = component.strip()
            if component[0] != self.ins_data.quote or component[-1] != self.ins_data.quote:
                continue
            component = component.replace(self.ins_data.quote, str())
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

    def manage_roast(self, the_lines):
        result = list()

        separator = ' = '
        head = '[[package]]'
        for line in the_lines:
                if line.strip().find('name') != 0:
                    continue

                the_fields = line.split(separator)
                if len(the_fields) == 2:
                    component = the_fields[1]
                    component = component.strip()
                    component = component.replace(self.ins_data.quote, str())
                    my_list = [component]
                    result.append(my_list)

        return result

    def check_allowed_characters_in_string(self, my_string, the_allowed_characters):
        number_found = True

        for c in my_string:
            if c not in the_allowed_characters:
                number_found = False
                break

        return number_found

    def get_min_of_indent(self, the_lines):
        n = 999
        previous_n = 999

        space = ' '
        tab = '\t'
        the_values = [space, tab]
        for line in the_lines:
            if line == str(): continue
            if line[0] not in the_values: continue

            n = 0
            for c in line:
                if c in the_values:
                    n += 1
                else:
                    break

            n = min(previous_n, n)
            previous_n = n + 0

        return n

    def version_valid(self, value):
        result = True

        if '$' in value: return True

        value = value.replace('^', str())
        value = value.replace('.', str())
        value = value.replace('+', str())
        for c in value:
            if c not in self.ins_data.the_numbers:
                result = False
                break

        return result

    def extract_the_blocks_for_flutter(self, the_lines):
        result = list()

        space = ' '
        tabulation = '\t'
        block_found = False
        for i in range(0, len(the_lines)):
            line = the_lines[i]

            # head
            if block_found == False:
                if line in self.the_heads:
                    block_found = True
                    continue

            #foot: empty line
            new_line = line.strip()
            if new_line == str():
                block_found = False
                continue

            #foot: first character
            if (line[0] != space) and (line[0] != tabulation):
                block_found = False
                continue

            #enough characters in the line ?
            if len(new_line) < 2:
                continue

            if block_found == True:
                result.append(line)

        return result

    def get_data_for_flutter(self, the_lines):
        result = list()

        space = ' '
        tabulation = '\t'
        the_prefixes = [space, space + space, tabulation]
        for i in range(0, len(the_lines)):
            line = the_lines[i]
            if ':' not in line:
                continue

            to_treat = False
            if line[0] == tabulation:
                if line[1] not in the_prefixes:
                    to_treat = True
            elif line[0] == space:
                if line[1] not in the_prefixes:
                    to_treat = True
                elif line[1] == space:
                    if line[2] not in the_prefixes:
                        to_treat = True

            if to_treat == False:
                continue

            value = the_lines[i].strip()
            p = value.find(':')
            value = value[:p]
            my_list = [value]
            result.append(my_list)

        return result

    def manage_go(self, the_lines):
        result = list()

        for line in the_lines:
            line_with_indirect = line.replace(' ', '')
            if '//indirect' in line_with_indirect:
                continue

            new_line = line.strip()
            the_fields = new_line.split(' ')
            component = the_fields[0]
            my_list = [component]
            result.append(my_list)

        return result

    def manage_swift(self, the_lines):
        result = list()

        prefix = '.package'
        quote = '\"'
        for line in the_lines:
            p = line.find(prefix)
            if p < 0: continue

            p = line.find('url:')
            if p < 0: continue
            line = line[p:]

            p = line.find(quote)
            line = line[p+1:]
            p = line.find(quote)
            line = line[:p]

            component = line.strip()
            the_websites = ['https://github.com', 'http://github.com']
            website_found = False
            for website in the_websites:
                if component.find(website) == 0:
                    website_found = True
                    break
            if website_found == False: continue

            my_list = [component]
            result.append(my_list)

        return result

    def get_data_for_cocoapods(self, the_lines):
        result = list()

        the_quotes = ['\'', '\"']
        for line in the_lines:
            new_line = line.strip()
            if new_line.find('pod') == 0:
                for quote in the_quotes:
                    p = new_line.find(quote)
                    if p > -1:
                        new_line = new_line[p +1:]
                        p = new_line.find(quote)
                        dependency = new_line[:p]
                        result.append([dependency])

        return result

    def manage_elm_lang(self, the_lines):
        result = list()

        for line in the_lines:
            component = line.strip()
            component = component[1:]
            p = component.find('\"')
            component = component[:p]
            my_list = [component]
            result.append(my_list)

        return result

    def get_the_dependencies_on_error(self, platform, the_lines_on_error, separator_between_fields_in_file):
        the_dependencies_on_error = list()

        for line in the_lines_on_error:
            if separator_between_fields_in_file in line:
                the_values = line.split(separator_between_fields_in_file)
                the_dependencies_on_error.append(the_values[1:])

        return the_dependencies_on_error

    def route(self, language, the_lines, ins_filter):
        result = list()

        self.the_lines = the_lines
        ins_name = CName()

        if language == ins_name.gradle:
            result = self.manage_gradle(the_lines)
        elif language == ins_name.package_json:
            result = self.manage_package_json(the_lines)
        elif language == ins_name.roast:
            result = self.manage_roast(the_lines)
        elif language == ins_name.go:
            result = self.manage_go(the_lines)
        elif language == ins_name.flutter:
            result = self.get_data_for_flutter(the_lines)
        elif language == ins_name.swift:
            result = self.manage_swift(the_lines)
        elif language == ins_name.cocoapods:
            result = self.get_data_for_cocoapods(the_lines)

        return result
