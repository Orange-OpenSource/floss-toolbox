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
from unittest.mock import patch

import os

from sources.common import CFilter, CName
from sources.configuration import CConfig
from sources.dependencies import CDependencies


class TestDependencies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        cls.path = my_path

        path_data = os.path.join(my_path, "data")
        cls.path_data = path_data

    def test_configuration(self):
        ins_config = CConfig()
        ins_config.path = self.path_data
        ins_config.filename = 'config.ini'

        ins_config.get_the_config()

        expected = './foo-test'
        self.assertEqual(expected, ins_config.path_dependencies)
        expected = ['f_a.ext', 'f_b.ext']
        self.assertEqual(expected, ins_config.the_filenames)
        expected = './foo-test/licenses'
        self.assertEqual(expected, ins_config.path_licenses)

    def test_configuration_bad_path(self):
        ins_config = CConfig()
        ins_config.path = self.path
        ins_config.filename = 'config.ini'

        try:
            ins_config.get_the_config()
        except Exception as e:
            value = '\t💥  read_text_file: no file to read.'
            self.assertEqual(e.__str__(), value)

    def test_configuration_empty_file(self):
        ins_config = CConfig()
        ins_config.path = self.path_data
        ins_config.filename = 'config_empty.ini'

        try:
            ins_config.get_the_config()
        except Exception as e:
            value = '\t💥  The path containing the dependencies is not found in the ini file'
            self.assertEqual(e.__str__(), value)

    def test_configuration_no_data(self):
        ins_config = CConfig()
        ins_config.path = self.path_data

        ins_config.filename = 'config_no_path_to_parse.ini'
        try:
            ins_config.get_the_config()
        except Exception as e:
            value = '\t💥  At least, 1 line is not well formatted.'
            self.assertEqual(e.__str__(), value)

        ins_config.filename = 'config_no_file.ini'
        try:
            ins_config.get_the_config()
        except Exception as e:
            value = '\t💥  the filenames containing the dependencies are not found in the ini file'
            self.assertEqual(e.__str__(), value)

        ins_config.filename = 'config_no_path_licenses.ini'
        try:
            ins_config.get_the_config()
        except Exception as e:
            value = '\t💥  The path to store the licenses is not found in the ini file'
            self.assertEqual(e.__str__(), value)
