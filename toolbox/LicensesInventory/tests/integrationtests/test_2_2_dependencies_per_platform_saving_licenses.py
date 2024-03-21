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

    @patch('requests.get')
    def test_new_dependencies(self, mock_requests_get):

        ins_config = CConfig()
        ins_config.path = self.path_data
        ins_config.filename = 'config_3.ini'
        ins_config.get_the_config()

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        ins_dependencies = CDependencies()
        the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)
        self.assertEqual(7, len(the_dependencies_by_platform))

        number = 2
        the_d = the_dependencies_by_platform[CName().cocoapods]
        self.assertEqual(number, len(the_d))
        the_d = the_dependencies_by_platform[CName().flutter]
        self.assertEqual(number, len(the_d))
        the_d = the_dependencies_by_platform[CName().go]
        self.assertEqual(number, len(the_d))
        the_d = the_dependencies_by_platform[CName().package_json]
        self.assertEqual(number, len(the_d))
        the_d = the_dependencies_by_platform[CName().roast]
        self.assertEqual(number, len(the_d))
        the_d = the_dependencies_by_platform[CName().swift]
        self.assertEqual(number, len(the_d))
        the_d = the_dependencies_by_platform[CName().gradle]
        self.assertEqual(number, len(the_d))

        # requests
        import requests
        response = requests.models.Response
        response.status_code = '200'
        response.text = 'line_a\nline_b'
        #head = '<h1>License</h1>'
        mock_requests_get.return_value = response

        from sources.search import CSearch
        r = CSearch().get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, the_new_dependencies_on_error_by_platform = r

        self.assertEqual(7, len(the_licenses_by_platform))
        self.assertEqual(0, len(the_new_dependencies_on_error_by_platform))

        from sources.common import CFile
        CFile().save_the_licenses(the_licenses_by_platform, ins_config)
        CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)
