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
import time
import math

path = os.getcwd()
sys.path.insert(1, path)

from sources.configuration import CConfig
from sources.common import CFilter
from sources.dependencies import CDependencies
from sources.search import CSearch
from sources.common import CFile

def get_the_lines(the_licenses_by_platform):
    """
    Helps to build the final output file with for each dependency its license

    :param the_licenses_by_platform: Object containing the licenses and dependencies
    """

    print('\t➡️  Getting the lines...')
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

    print('\t\t✅ Getting the lines... OK!')
    return the_lines

def main():
    """
    Initializes all configuration objects.
    The get the configuration items from the config file.
    After that parse the dependencies manager file(s), extract dependencies, get licences and write final file.
    """

    print('➡️  Preparing CConfig()...')
    ins_config = CConfig()

    print('➡️  Preparing CFilter()...')
    ins_filter = CFilter()

    print('➡️  Preparing CDependencies()...')
    ins_dependencies = CDependencies()

    print('➡️  Preparing CSearch()...')
    ins_search = CSearch()

    print('➡️  Preparing CFile()...')
    ins_file = CFile()

    print('➡️  Getting the config...')
    ins_config.get_the_config()

    print('➡️  Preparing stuff...')
    ins_filter.prepare(ins_config)

    print('🎯 Getting the dependencies...')
    the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)
    if len(the_dependencies_by_platform) == 0:
        print('⚠️  No dependencies found!')
        raise Exception('\t💥  Unable to go further, missing data (dependencies) to process.')

    print('🎯 Getting the licences...')
    the_licenses_by_platform = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
    if len(the_licenses_by_platform) == 0:
        print('⚠️  No licenses by platform found!')
        raise Exception('\t💥  Unable to go further, missing data (licenses by plaform) to process.')

    print('🎯 Getting the lines...')
    the_lines = get_the_lines(the_licenses_by_platform)

    print('-----------------------')
    print('📣 Here are the results!')
    if len(the_lines) == 0:
        print('⚠️  No license')
        the_lines = ['No license']

    ins_file.write_in_text_file(ins_config.path_licenses, 'licenses.txt', the_lines)
    print('🎉 Found ', len(the_lines), " dependencies and licenses ! 🎉 ")
    print('🔍 See the file at ', ins_config.path_licenses, 'to get details.')

if __name__ == "__main__":
    try:
        start = time.time()
        main()
        end = time.time()
        print("⏱️  Elasped time: ", math.ceil(end - start), " seconds")
        print('👋 See you later!')
    except Exception as e:
        print('💥  main:', e.__str__())
