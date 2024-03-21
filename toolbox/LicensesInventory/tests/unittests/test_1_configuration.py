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

from sources.common import CFilter, CName
from sources.configuration import CConfig
from sources.dependency import CDependencies


class TestConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")

        cls.path_tests = os.path.join(path_data, "config_ini")
        cls.path_dependencies = 'path_dependencies'
        cls.the_filenames = ['a', 'b']
        cls.path_licenses ='path_licenses'

    def check(self, path_for_tests, filename_for_tests, expected_path_dependencies, expected_the_filenames, expected_path_licenses):
        ins_config = CConfig()
        ins_config.path = path_for_tests
        ins_config.filename = filename_for_tests
        ins_config.get_the_config()

        self.assertEqual(expected_path_dependencies, ins_config.path_dependencies)
        self.assertEqual(expected_the_filenames, ins_config.the_filenames)
        self.assertEqual(expected_path_licenses, ins_config.path_licenses)

    def test_ok(self):
        path = self.path_tests
        filename = 'config.ini'
        expected_path_dependencies = self.path_dependencies
        expected_the_filenames = self.the_filenames
        expected_path_licenses = self.path_licenses
        self.check( path, filename, expected_path_dependencies, expected_the_filenames, expected_path_licenses)

    def test_file_empty(self):
        path = self.path_tests
        filename = 'config_empty.ini'
        expected_path_dependencies = str()
        expected_the_filenames = list()
        expected_path_licenses = str()
        self.check( path, filename, expected_path_dependencies, expected_the_filenames, expected_path_licenses)

    def test_no_path_dependencies(self):
        path = self.path_tests
        filename = 'config_no_path_to_parse.ini'
        expected_path_dependencies = str()
        expected_the_filenames = self.the_filenames
        expected_path_licenses = self.path_licenses
        self.check( path, filename, expected_path_dependencies, expected_the_filenames, expected_path_licenses)

    def test_no_filename(self):
        path = self.path_tests
        filename = 'config_no_file.ini'
        expected_path_dependencies = self.path_dependencies
        expected_the_filenames = list()
        expected_path_licenses = self.path_licenses
        self.check( path, filename, expected_path_dependencies, expected_the_filenames, expected_path_licenses)

    def test_no_path_licenses(self):
        path = self.path_tests
        filename = 'config_no_path_licenses.ini'
        expected_path_dependencies = self.path_dependencies
        expected_the_filenames = self.the_filenames
        expected_path_licenses = str()
        self.check( path, filename, expected_path_dependencies, expected_the_filenames, expected_path_licenses)

    def test_no_file(self):
        ins_config = CConfig()
        ins_config.path = self.path_tests
        filename = '9999'
        ins_config.filename = filename
        try:
            ins_config.get_the_config()
            self.fail()
        except Exception as e:
            pass
