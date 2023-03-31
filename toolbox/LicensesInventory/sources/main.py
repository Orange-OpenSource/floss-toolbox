#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import sys
import os

path = os.getcwd()
sys.path.insert(1, path)

from sources.configuration import CConfig
from sources.common import CFilter
from sources.dependencies import CDependencies
from sources.search import CSearch
from sources.common import CFile


def get_the_lines(the_licenses_by_platform):
    the_lines = list()

    separator = ' : '
    for platform, the_licenses in the_licenses_by_platform.items():
        for license in the_licenses:
            line = str()
            for field in license:
                if field == None or field == str():
                    field = 'None'
                if line == str():
                    line = field
                else:
                    line += separator + field
            the_lines.append(line)

    return the_lines

def main():
    ins_config = CConfig()
    ins_filter = CFilter()
    ins_dependencies = CDependencies()
    ins_search = CSearch()
    ins_file = CFile()

    ins_config.get_the_config()
    ins_filter.prepare(ins_config)
    the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)
    the_licenses_by_platform = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
    the_lines = get_the_lines(the_licenses_by_platform)
    if len(the_lines) == 0:
        print('No license')
        the_lines = ['No license']
    ins_file.write_in_text_file(ins_config.path_licenses, 'licenses.txt', the_lines)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('main:', e.__str__())
