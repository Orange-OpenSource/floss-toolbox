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


def main():
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
    r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
    the_licenses_by_platform, on_error = r
    if len(the_licenses_by_platform) == 0:
        print('⚠️  No licenses by platform found!')
        raise Exception('\t💥  Unable to go further, missing data (licenses by plaform) to process.')

    print('🎯 Saving the licenses...')
    ins_file.save_the_licenses(the_licenses_by_platform, ins_config.path_licenses)

    print('🎯 Saving the errors...')
    ins_file.save_the_errors(on_error, ins_config.path, ins_config.filename_for_the_errors)


if __name__ == "__main__":
    try:
        start = time.time()
        main()
        end = time.time()
        print("⏱️  Elasped time: ", math.ceil(end - start), " seconds")
        print('👋 Please, check all the results (licenses, versions and count) of dependancies. See you later!')
    except Exception as e:
        print('💥  main:', e.__str__())
        print('Maybe you should run the tests or check your network configuration (e.g. proxys or firewalls)')