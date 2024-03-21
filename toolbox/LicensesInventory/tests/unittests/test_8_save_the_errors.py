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
from unittest.mock import patch, Mock

import os

from sources.common import CFile
from sources.configuration import CConfig


class TestFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        path_tests = os.path.join(path_data, "save")
        cls.path = path_tests

    @patch('os.rename')
    @patch('os.remove')
    @patch('sources.common.files.CFile.write_in_text_file')
    def test_no_error(self, mock_write, mock_remove, mock_rename):
        platform = 'p_a'
        mock_rename.reset
        mock_write.reset
        mock_remove.reset

        the_new_dependencies_on_error_by_platform = dict()

        path = os.path.join(self.path, 'errors_no_file')
        ins_config = CConfig()
        ins_config.path_errors = path

        r = CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)

        mock_rename.assert_not_called()
        mock_write.assert_not_called()
        mock_remove.assert_not_called()

        # the file already exists
        path = os.path.join(self.path, 'errors_file')
        ins_config = CConfig()
        ins_config.path_errors = path

        r = CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)

        mock_rename.assert_not_called()
        mock_write.assert_not_called()
        mock_remove.assert_not_called()

    def assert_the_lines(self, r, the_expected):
        for i in range(0, len(the_expected)):
            self.assertEqual(the_expected[i], r[i], i)

    @patch('sources.common.dates_and_times.CDate.get_date_and_time')
    @patch('os.rename')
    @patch('os.remove')
    @patch('sources.common.files.CFile.write_in_text_file', side_effect=['a', 'b'])
    def test_the_errors(self, mock_write, mock_remove, mock_rename, mock_date):
        the_platforms = ['p_a', 'p_b']
        path = os.path.join(self.path, 'errors_file')
        ins_config = CConfig()
        ins_config.path_errors = path
        date_for_test = 'date for test'
        mock_date.return_value = date_for_test

        r = get_the_data(the_platforms, date_for_test)
        the_new_dependencies_on_error_by_platform, filename_a, the_lines_a, filename_b, the_lines_b = r

        r = CFile().save_the_errors(the_new_dependencies_on_error_by_platform, ins_config)
        self.assertEqual(1, len(mock_date.mock_calls))
        self.assertEqual(2, len(mock_rename.mock_calls))
        self.assertEqual(2, len(mock_remove.mock_calls))
        self.assertEqual(2, len(mock_write.mock_calls))

        self.assert_the_lines(r, the_lines_a + the_lines_b)

        mock_write.assert_any_call(ins_config.path_errors, filename_a, the_lines_a)
        mock_write.assert_any_call(ins_config.path_errors, filename_b, the_lines_b)

def get_the_data(the_platforms, date_for_test):
    the_new_dependencies_on_error_by_platform = dict()

    # file 1
    old_lines_a = ['Date: 1111-11-11T11:11:11']
    old_lines_a += ['error code = 411 : c_11 : n_11']

    new_lines_a = ['Date: ' + date_for_test]
    ## already exists
    the_values_a = ['error code = 411', 'c_11', 'n_11']
    new_lines_a += ['error code = 411 : c_11 : n_11']
    ## new
    the_values_b = ['error code = 419', 'c_19', 'n_19']
    new_lines_a += ['error code = 419 : c_19 : n_19']

    # file 2
    old_lines_b = ['Date: 2222-22-22T22:22:22']
    old_lines_b += ['error code = 421 : c_21']
    old_lines_b += ['Date: 3333-33-33T33:33:33']
    old_lines_b += ['error code = 431 : c_31']
    old_lines_b += ['error code = 432 : c_32']

    new_lines_b = ['Date: ' + date_for_test]
    ## already exist
    the_values_c = ['error code = 431', 'c_31']
    new_lines_b += ['error code = 431 : c_31']
    ## new
    the_values_d = ['error code = 429', 'c_29']
    new_lines_b += ['error code = 429 : c_29']
    the_values_e = ['error code = 439', 'c_39']
    new_lines_b += ['error code = 439 : c_39']

    filename_a = 'errors_p_a.txt'
    filename_b = 'errors_p_b.txt'
    the_lines_a = old_lines_a + new_lines_a
    the_lines_b = old_lines_b + new_lines_b
    the_new_dependencies_on_error_by_platform[the_platforms[0]] = [the_values_a, the_values_b]
    the_new_dependencies_on_error_by_platform[the_platforms[1]] = [the_values_c, the_values_d, the_values_e]

    return (the_new_dependencies_on_error_by_platform, filename_a, the_lines_a, filename_b, the_lines_b)