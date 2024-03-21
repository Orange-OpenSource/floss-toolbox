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

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

from sources.common import CFilter, CName, CChoice
from sources.configuration import CConfig
from sources.dependency import CDependencies


class TestDependencies(unittest.TestCase):

    """
    Tests with real data
    """

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        cls.path_data = os.path.join(my_path, "real_data")

        the_filenames = ['Podfile', 'pubspec.yaml', 'go.mod', 'Cargo.lock']
        the_filenames += ['build.gradle', 'build.gradle.kts', 'package.json', 'Package.swift']
        cls.the_filenames = the_filenames

    def test_new_dependencies(self):

        ins_config = CConfig()
        ins_config.path = self.path_data
        ins_config.filename = "config.ini"
        ins_config.get_the_config()

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
        if the_dependencies_by_platform == None: #the user choose to quit
            self.fail()
        self.assertEqual(7, len(the_dependencies_by_platform))

        the_d = the_dependencies_by_platform[CName().cocoapods]
        self.assertEqual(7, len(the_d))
        the_d = the_dependencies_by_platform[CName().flutter]
        self.assertEqual(50, len(the_d))
        the_d = the_dependencies_by_platform[CName().go]
        self.assertEqual(17, len(the_d))
        the_d = the_dependencies_by_platform[CName().package_json]
        self.assertEqual(41, len(the_d))
        the_d = the_dependencies_by_platform[CName().roast]
        self.assertEqual(124, len(the_d))
        the_d = the_dependencies_by_platform[CName().swift]
        self.assertEqual(7, len(the_d))
        the_d = the_dependencies_by_platform[CName().gradle]
        self.assertEqual(18, len(the_d))

