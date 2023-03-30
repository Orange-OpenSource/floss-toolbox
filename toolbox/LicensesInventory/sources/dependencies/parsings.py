#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..common import CFile
from ..common import CFilter
from ..common import CData
from ..common import CName


class CParsing:

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

    def get_min_of_indent(self, the_lines):
        n = 999
        previous_n = 999

        space = ' '
        tab = '\t'
        the_values = [' ', '\t']
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

    def get_data_for_flutter(self, the_lines):
        result = list()

        the_lines = self.get_the_lines_for_flutter(the_lines)
        indent_mini = self.get_min_of_indent(the_lines)
        if indent_mini == 0: return result
        space = ' '
        tabulation = '\t'

        for i in range(0, len(the_lines)):
            line = the_lines[i]

            #check it is a line to keep
            after_space = line[indent_mini]
            if (after_space == space) or (after_space == tabulation):
                continue

            new_line = line.strip()
            the_fields = new_line.split(':')
            component = the_fields[0]
            version = the_fields[1].strip()

            component_found = False
            if self.version_valid(version) == True:
                component_found = True
            elif version == str():
                component_found = True

            if component_found == True:
                my_list = [component]
                result.append(my_list)

        return result

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

    def get_the_lines_for_flutter(self, the_lines):
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

            # foot
            new_line = line.strip()
            if new_line == str():
                block_found = False
                continue

            # good data
            if block_found == True:
                result.append(line)

        return result

    def manage_go(self, the_lines):
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
        result = list()

        for line in the_lines:
            p = line.find('.package')
            if p != 0: continue
            p = line.find('url:')
            if p < 0: continue
            line = line[p:]

            p = line.find('\"')
            line = line[p+1:]
            p = line.find('\"')
            line = line[:p]

            component = line.strip()
            if component.find('https') != 0: continue
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
        elif language == ins_name.cocoapods:
            result = self.get_data_for_cocoapods(the_lines)
        elif language == ins_name.elm_lang:
            r = self.get_data(0, 1)
            the_lines, i = r
            result = self.manage_elm_lang(the_lines)

        return result
