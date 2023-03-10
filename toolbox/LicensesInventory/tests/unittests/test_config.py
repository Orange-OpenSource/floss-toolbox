# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import unittest
from unittest.mock import patch
import sys
import os

from sources.configuration import CConfig
from sources.common import CFile, CName

class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup data for the tests
        """
        my_path = os.path.dirname(os.path.realpath(__file__))
        my_path_data = os.path.join(my_path, "data")
        #cls.path_data = my_path_data

        #cls.filename = os.path.join(my_path_data, "config.ini")

        ins_config = CConfig()
        cls.ins_config = ins_config

    def test_extract_data_from_ini_file(self):
        label_dependencies = 'path to parse'
        path_dependencies = os.path.dirname(os.path.realpath(__file__))
        label_the_filenames = 'list of the files'
        the_filenames = ['file_a', 'file_b']
        label_licenses = 'path to store the licenses'
        path_licenses = os.path.dirname(os.path.realpath(__file__))

        separator = self.ins_config.separator
        the_lines = list()
        the_lines.append('[dependencies]')

        the_lines.append(label_dependencies + separator + path_dependencies)
        the_lines.append(label_licenses + separator + path_licenses)
        value = str()
        for filename in the_filenames:
            if value == str():
                value = filename
            else:
                value += ', ' + filename
        the_lines.append(label_the_filenames + separator + value)

        self.ins_config.extract_data_from_ini_file(the_lines)

        self.assertEqual (self.ins_config.path_dependencies, path_dependencies)
        self.assertEqual (self.ins_config.path_licenses, path_licenses)
        self.assertEqual (self.ins_config.the_filenames, the_filenames)

