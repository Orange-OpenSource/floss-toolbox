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


class TestLicenses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        path_tests = os.path.join(path_data, "save")
        cls.path = path_tests
        cls.comment_for_licenses = '# If the license is at None, or not clear, you are invited to search in the downloaded file.'
        cls.date_for_test = 'date for test'

    @patch('os.rename')
    @patch('os.remove')
    @patch('sources.common.files.CFile.write_in_text_file')
    def test_no_license(self, mock_write, mock_remove, mock_rename):
        platform = 'p_a'
        mock_rename.reset
        mock_write.reset
        mock_remove.reset

        the_licenses_by_platform = dict()

        ins_config = CConfig()
        ins_config.path_licenses = 'a path'

        r = CFile().save_the_licenses(the_licenses_by_platform, ins_config)

        mock_rename.assert_not_called()
        mock_write.assert_not_called()
        mock_remove.assert_not_called()

        # the file already exists
        the_licenses_by_platform = dict()

        ins_config = CConfig()
        ins_config.path_licenses = os.path.join(self.path, 'licenses_file')

        r = CFile().save_the_licenses(the_licenses_by_platform, ins_config)

        mock_rename.assert_not_called()
        mock_write.assert_not_called()
        mock_remove.assert_not_called()

    @patch('sources.common.dates_and_times.CDate.get_date_and_time')
    @patch('os.rename')
    @patch('os.remove')
    @patch('sources.common.files.CFile.write_in_text_file', side_effect=['a', 'b'])
    def test_the_licenses(self, mock_write, mock_remove, mock_rename, mock_date):
        the_platforms = ['p_a', 'p_b']

        the_licenses_by_platform = self.prepare(the_platforms)

        ins_config = CConfig()
        path = os.path.join(self.path, 'licenses_file')
        ins_config.path_licenses = path

        mock_date.return_value = self.date_for_test
        r = CFile().save_the_licenses(the_licenses_by_platform, ins_config)

        self.assertEqual(1, len(mock_date.mock_calls))

        self.check_mocks(mock_rename, mock_remove, mock_write, ins_config, 'licenses_p_a.txt')
        self.check_mocks(mock_rename, mock_remove, mock_write, ins_config, 'licenses_p_b.txt')

    def prepare(self, the_platforms):
        the_licenses_by_platform = dict()

        # file 1
        ## already exists
        the_new_licenses_a = [['c_11', 'n_11', 'license_11']]
        ## new
        the_new_licenses_a.append(['c_19', 'n_19', 'license_19'])

        # file 2
        ## already exist
        the_new_licenses_b = [['c_31', 'license_31']]
        ## new
        the_new_licenses_b.append(['c_29', 'license_29'])
        the_new_licenses_b.append(['c_39', 'license_39'])

        platform = the_platforms[0]
        the_licenses_by_platform[platform] = the_new_licenses_a
        platform = the_platforms[1]
        the_licenses_by_platform[platform] = the_new_licenses_b

        return the_licenses_by_platform

    def get_the_lines(self, date_for_test, comment):
        # file 1
        the_old_lines_a = [comment]
        the_old_lines_a += [CDate().prefix_for_date + '1111-11-11T11:11:11']
        the_old_lines_a += ['c_11 : n_11 : license_11']

        the_expected_lines_a = [CDate().prefix_for_date + date_for_test]
        ## already exists
        #the_new_licenses_a = [['c_11', 'n_11', 'license_11']]
        the_expected_lines_a += ['c_11 : n_11 : license_11']
        ## new
        #the_new_licenses_a.append(['c_19', 'n_19', 'license_19'])
        the_expected_lines_a += ['c_19 : n_19 : license_19']

        # file 2
        the_old_lines_b = [comment]
        the_old_lines_b += [CDate().prefix_for_date + '2222-22-22T22:22:22']
        the_old_lines_b += ['c_21 : license_21']
        the_old_lines_b += ['Date: 3333-33-33T33:33:33']
        the_old_lines_b += ['c_31 : license_31']
        the_old_lines_b += ['c_32 : license_32']

        the_expected_lines_b = [CDate().prefix_for_date + date_for_test]
        ## already exist
        #the_new_licenses_b = [['c_31', 'license_31']]
        the_expected_lines_b += ['c_31 : license_31']
        ## new
        #the_new_licenses_b.append(['c_29', 'license_29'])
        the_expected_lines_b += ['c_29 : license_29']
        #the_new_licenses_b.append(['c_39', 'license_39'])
        the_expected_lines_b += ['c_39 : license_39']

        return (the_old_lines_a, the_expected_lines_a, the_old_lines_b, the_expected_lines_b)

    def get_the_expected_filenames(self, ins_config, filename):
        file = os.path.join(ins_config.path_licenses, filename)
        renamed_filename = filename.replace('.txt', '.old')
        renamed_file = os.path.join(ins_config.path_licenses, renamed_filename)

        return (file, renamed_file)


    def check_mocks(self, mock_rename, mock_remove, mock_write, ins_config, filename):
        r = self.get_the_expected_filenames(ins_config, filename)
        file, renamed_file = r

        self.assertEqual(2, len(mock_rename.mock_calls))
        mock_rename.assert_any_call(file, renamed_file)

        self.assertEqual(2, len(mock_remove.mock_calls))
        mock_remove.assert_any_call(renamed_file)

        self.assertEqual(2, len(mock_write.mock_calls))
        # check in test_all

