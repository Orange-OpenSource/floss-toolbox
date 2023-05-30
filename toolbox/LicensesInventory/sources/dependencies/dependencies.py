#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

from ..common import CName
from sources.dependencies import CParsing

class CDependencies:

    def __init__(self):
        self.ins_name = CName()
        self.ins_filter = None
        self.ins_parsing = CParsing()
        #self.the_heads = list()
        #self.the_foots = list()

    def delete_the_duplicated(self, the_dependencies_by_platform):
        print('\t➡️  Deleting the duplicated...')
        result = dict()

        separator = ':::'
        for platform, the_dependencies in the_dependencies_by_platform.items():
            dict_a = dict()
            for dependency in the_dependencies:
                key = str()
                for value in dependency:
                    if key == str():
                        key = value
                    else:
                        key += separator + value
                dict_a[key] = 'ok'

            # sort data for the current platform
            the_keys = dict_a.keys()
            the_sorted = sorted(the_keys)

            # replace the data in the the new dict
            the_new_dependencies = list()
            for key in the_sorted:
                new_dependency = list()
                the_fields = key.split(separator)
                for i in range(0, len(the_fields)):
                    value = the_fields[i]
                    new_dependency.append(value)
                the_new_dependencies.append(new_dependency)

            result[platform] = the_new_dependencies

        return result

    def get_the_dependencies(self, ins_filter):
        print('\t➡️  Getting the dependencies...')   
        result = dict()

        self.ins_filter = ins_filter
        r = dict()
        for platform, the_lines in ins_filter.the_contents.items():
            if len(the_lines) == 0:
                continue
            the_lines = ins_filter.filter(the_lines, platform)
            self.ins_parsing.the_heads = ins_filter.the_heads[platform]
            self.ins_parsing.the_foots = ins_filter.the_foots[platform]

            the_dependencies = self.ins_parsing.get_the_values(platform, the_lines, ins_filter)
            result[platform] = the_dependencies

        result = self.delete_the_duplicated(result)
        return result
