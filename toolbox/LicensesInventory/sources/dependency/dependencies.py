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

from sources.common import CName, CDate, CFile
from sources.dependency import CParsing
from sources.common import CChoice, CPrompt
ins_prompt = CPrompt()


class CDependencies:

    def __init__(self):
        self.ins_name = CName()
        self.ins_filter = None
        self.ins_parsing = CParsing()
        self.ins_choice = CChoice()
        self.choice = dict()

    def delete_the_duplicated(self, the_dependencies_by_platform):
        result = dict()

        separator = ':::'
        for platform, the_dependencies in the_dependencies_by_platform.items():
            the_new_dependencies = list()
            for i_dependency in range(0, len(the_dependencies)):
                my_copy = the_dependencies[i_dependency + 1:]
                if the_dependencies[i_dependency] not in my_copy:
                    the_new_dependencies.append(the_dependencies[i_dependency])
            result[platform] = the_new_dependencies

        return result

    def get_the_data(self, ins_filter, the_lines_by_platform):
        result = dict()

        for platform, the_lines in the_lines_by_platform.items():
            self.ins_parsing.the_heads = ins_filter.the_heads[platform]
            self.ins_parsing.the_foot = ins_filter.the_foot[platform]
            the_new_dependencies = self.ins_parsing.route(platform, the_lines, ins_filter)
            result[platform] = the_new_dependencies

        return result

    def get_the_data_on_error(self, the_lines_by_platform):
        result = dict()

        for platform, the_lines in the_lines_by_platform.items():
            the_dependencies = list()

            for line in the_lines:
                if CDate().prefix_for_date in line: continue
                the_fields = line.split(CFile().separator)
                if len(the_fields) < 2: continue
                dependency = [the_fields[1]]
                if len(the_fields) > 2:
                    dependency += [the_fields[2]]
                the_dependencies.append(dependency)

            result[platform] = the_dependencies

        return result

    def display_dict(self, my_dict, indent):
        max_platform_size = 0
        for p, the_v in my_dict.items():
            max_platform_size = max(max_platform_size, len(the_v))

        for p, the_v in my_dict.items():
                s  = len(p)
                if s < max_platform_size:
                    number_of_spaces = ' ' * (max_platform_size - s)
                    p += number_of_spaces
                print(indent + p + ':', str(len(the_v)))

    def get_the_duplicated(self, the_dependencies_on_error_by_platform, the_dependencies_by_platform):
        result = dict()

        if the_dependencies_by_platform == the_dependencies_on_error_by_platform:
            return result

        for platform, the_d_on_error in the_dependencies_on_error_by_platform.items():
            if platform not in the_dependencies_by_platform.keys(): continue
            the_d = the_dependencies_by_platform[platform]
            for d in the_d:
                if d not in the_d_on_error: continue
                if platform not in result.keys():
                    result[platform] = [d]
                else:
                    result[platform] += [d]

        return result

    def choice_the_data_to_treat(self, ins_filter, the_contents_on_error, the_contents):
        result = dict()

        the_dependencies_by_platform = self.get_the_data(ins_filter, the_contents)
        the_dependencies_by_platform = self.delete_the_duplicated(the_dependencies_by_platform)

        the_dependencies_on_error_by_platform = self.get_the_data_on_error(the_contents_on_error)
        the_dependencies_on_error_by_platform = self.delete_the_duplicated(the_dependencies_on_error_by_platform)

        if (len(the_dependencies_on_error_by_platform) == 0) and (len(the_dependencies_by_platform) == 0):
            raise Exception('No data to treat.')

        if (len(the_dependencies_on_error_by_platform) == 0) and (len(the_dependencies_by_platform) > 0):
            print('Treat the new dependencies. No dependency on error in the folder with the licenses.')
            return the_dependencies_by_platform

        if (len(the_dependencies_on_error_by_platform) > 0) and (len(the_dependencies_by_platform) == 0):
            print('Treat the dependencies on error. No new dependency.')
            return the_dependencies_on_error_by_platform

        # new dependencies and dependencies on error
        indent = '  '
        print('The new dependencies to treat:')
        self.display_dict(the_dependencies_by_platform, indent)
        print('The dependencies on error:')
        self.display_dict(the_dependencies_on_error_by_platform, indent)

        the_duplicated_by_platform = self.get_the_duplicated(the_dependencies_on_error_by_platform, the_dependencies_by_platform)
        if len(the_duplicated_by_platform) > 0:
            print('Duplicated dependencies are found:')
            self.display_dict(the_duplicated_by_platform, indent)

        choice = ins_prompt.choose_the_data_to_treat()
        if choice == CChoice().quit:
            return None

        if choice == self.ins_choice.only_the_new_dependencies:
                return the_dependencies_by_platform

        if choice == CChoice().only_the_dependencies_on_error:
            return the_dependencies_on_error_by_platform

    def get_the_dependencies(self, ins_filter):
        the_data_by_platform = self.choice_the_data_to_treat(ins_filter, ins_filter.the_contents_on_error, ins_filter.the_contents)
        if the_data_by_platform == None: return None
        return the_data_by_platform

