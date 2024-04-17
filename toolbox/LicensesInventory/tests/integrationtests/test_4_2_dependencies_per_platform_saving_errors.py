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
    Before to test the saving of the dependencies on error, in integrationtests, delete the files in:
     licenses_with_errors
     licenses_with_retry_after
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
        ins_config.filename = 'config_2.ini'
        ins_config.get_the_config()

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        ins_dependencies = CDependencies()
        the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)
        if the_dependencies_by_platform == None:
            return
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
        response.status_code = '300'
        response.text = 'line_a\nline_b'
        mock_requests_get.return_value = response

        from sources.search import CSearch
        ins_search = CSearch()
        r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)

        the_licenses_by_platform, the_new_dependencies_on_error_by_platform = r
        self.assertEqual(0, len(the_licenses_by_platform))
        self.assertEqual(7, len(the_new_dependencies_on_error_by_platform))

        from sources.common import CFile
        CFile().save_the_licenses(the_licenses_by_platform, ins_config)
        CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)

    @patch('requests.get')
    def test_new_dependencies_with_retry_after(self, mock_requests_get):

        ins_config = CConfig()
        ins_config.path = self.path_data
        ins_config.filename = 'config_2_retry_after.ini'
        ins_config.get_the_config()

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        ins_dependencies = CDependencies()
        the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)
        if the_dependencies_by_platform == None:
            return
        self.assertEqual(7, len(the_dependencies_by_platform))

        number = 2
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
        response.status_code = '300'
        response.retry_after = 'Mon, 22 Feb 2024 17:00:00 GMT'
        response.text = 'line_a\nline_b'
        mock_requests_get.return_value = response

        from sources.search import CSearch
        ins_search = CSearch()
        r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)

        the_licenses_by_platform, the_new_dependencies_on_error_by_platform = r
        self.assertEqual(0, len(the_licenses_by_platform))
        self.assertEqual(7, len(the_new_dependencies_on_error_by_platform))

        from sources.common import CFile
        CFile().save_the_licenses(the_licenses_by_platform, ins_config)
        CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)
