# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import unittest
import os
from unittest.mock import Mock, MagicMock, patch

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
        cls.filename = 'files_read.txt'
        cls.filename_to_write = 'files_write.txt'
        cls.encoding='utf-8'

        cls.ins_files = CFile()

    def test_read_text_file(self):
        the_lines = self.ins_files.read_text_file (self.path_data, self.filename)
        self.assertEqual(2, len(the_lines))
        self.assertEqual('one', the_lines[0])
        self.assertEqual('two', the_lines[1])

    def test_read_text_file_bad_filename(self):
        the_lines = list()
        try:
            the_lines = self.ins_files.read_text_file (self.path_data, '')
            fail()
        except:
            pass

        try:
            the_lines = self.ins_files.read_text_file (self.path_data, None)
            fail()
        except:
            pass

    def test_read_text_file_bad_path(self):
        the_lines = list()
        try:
            the_lines = self.ins_files.read_text_file ('', self.filename)
            fail()
        except:
            pass

        try:
            the_lines = self.ins_files.read_text_file (None, self.filename)
            fail()
        except:
            pass

    def test_write_in_text_file_bad_path(self):
        the_lines = list()
        try:
            self.ins_files.write_in_text_file(None, self.filename, the_lines)
            fail()
        except:
            pass

        try:
            self.ins_files.write_in_text_file('', self.filename, the_lines)
            fail()
        except:
            pass

    def test_write_in_text_file_bad_filename(self):
        the_lines = list()

        try:
            self.ins_files.write_in_text_file(self.path_data, None, the_lines)
            fail()
        except:
            pass

        try:
            self.ins_files.write_in_text_file(self.path_data, '', the_lines)
            fail()
        except:
            pass
