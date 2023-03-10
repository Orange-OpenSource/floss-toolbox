# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import unittest
import os

from sources.common import CFile

class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup data for the tests
        """
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        cls.path_data = path_data
        cls.filename = 'filename_by_name.test'

        cls.ins_files = CFile()

    def test_get_the_files_by_names(self):
        the_files = self.ins_files.get_the_files_by_names(self.path_data, self.filename)

        self.assertEqual(1, len(the_files))
        expected = os.path.join(self.path_data, self.filename)
        self.assertEqual(True, expected == the_files[0])

    def test_get_the_files_by_names_no_path(self):
        the_files = list()

        try:
            the_files = self.ins_files.get_the_files_by_names('dddd', self.filename)
            fail()
        except:
            pass

        try:
            the_files = self.ins_files.get_the_files_by_names('', self.filename)
            fail()
        except:
            pass

        try:
            the_files = self.ins_files.get_the_files_by_names(None, self.filename)
            fail()
        except:
            pass

    def test_get_the_files_by_names_no_file(self):
        the_files = list()

        try:
            the_files = self.ins_files.get_the_files_by_names(self.path_data, 'ddd')
            fail()
        except:
            pass

        try:
            the_files = self.ins_files.get_the_files_by_names(self.path_data, '')
            fail()
        except:
            pass

        try:
            the_files = self.ins_files.get_the_files_by_names(self.path_data, None)
            fail()
        except:
            pass
