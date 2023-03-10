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

        cls.ins_files = CFile()

    def test_check_the_directory_no_path(self):
        try:
            result = self.ins_files.check_the_directory('dddd', False)
            fail()
        except Exception as e:
            pass

        try:
            result = self.ins_files.check_the_directory('', False)
            fail()
        except:
            pass

        try:
            result = self.ins_files.check_the_directory(None, False)
            fail()
        except:
            pass

    #@patch('sources.common.input')
    #def test_ask_before_creating_directory(self, mocked_os):
    #    path = os.path.join(self.path_data, 'new_folder')
    #
    #    mocked_os.return_value = 'o'
    #    result = self.ins_files.ask_before_creating_directory(path)
    #    mocked_os.assert_called()
    #    self.assertEqual(False, result)
    #
    #    mocked_os.return_value = 'y'
    #    result = self.ins_files.ask_before_creating_directory(path)
    #    mocked_os.assert_called()
    #    self.assertEqual(True, result)
    #
    #    mocked_os.return_value = 'Y'
    #    result = self.ins_files.ask_before_creating_directory(path)
    #    mocked_os.assert_called()
    #    self.assertEqual(True, result)

    @patch('os.makedirs')
    @patch('sources.common.CFile.ask_before_creating_directory')
    def test_check_the_directory_with_os_input(self, mock_for_ask, mock_for_makedir):
        path = os.path.join(self.path_data, 'new_folder')

        mock_for_ask.return_value = True
        result = self.ins_files.check_the_directory(path, True, True)
        mock_for_ask.assert_called()
        mock_for_makedir.assert_called()
        self.assertEqual(True, result)

        mock_for_ask.return_value = False
        try:
            result = self.ins_files.check_the_directory(path, True, True)
            fail()
        except:
            pass

