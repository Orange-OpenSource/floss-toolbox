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

import sys
import os

path = os.getcwd()
sys.path.insert(1, path)

from sources.configuration import CConfig
from sources.common import CFilter
from sources.dependency import CDependencies
from sources.search import CSearch
from sources.common import CFile


def main():
    ins_config = CConfig()
    ins_filter = CFilter()
    ins_dependencies = CDependencies()
    ins_search = CSearch()
    ins_file = CFile()

    ins_config.get_the_config()
    ins_filter.prepare(ins_config)

    the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
    if the_dependencies_by_platform == None: #the user choose to quit
        return

    r = CSearch().get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
    the_licenses_by_platform, the_new_dependencies_on_error_by_platform = r

    CFile().save_the_licenses(the_licenses_by_platform, ins_config)
    CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('main:', e.__str__())
