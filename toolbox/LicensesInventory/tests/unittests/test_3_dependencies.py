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
    test with new dependencies or dependencies on error:
        check if the data are extracted correctly
        check the duplicated
    tests with new dependencies and dependencies on error:
        the name of each dependency on error is prefixed by 'error_'
        check the choice of the user; new or on error ?
    """

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        path_tests = os.path.join(path_data, "get_the_dependencies")

        cls.path_no_file = os.path.join(path_tests, "no_file")
        cls.path_dependencies_empty = os.path.join(path_tests, "dependencies_empty")
        cls.path_dependencies = os.path.join(path_tests, "dependencies")
        cls.path_dependencies_on_error = os.path.join(path_tests, 'dependencies_on_error')

        ins_name = CName()

        the_filenames_by_platform = dict()
        the_filenames_by_platform[ins_name.gradle] = ['build.gradle.kts']
        the_filenames_by_platform[ins_name.package_json] = [ins_name.package_json]
        the_filenames_by_platform[ins_name.roast] = [ins_name.roast]
        the_filenames_by_platform[ins_name.go] = [ins_name.go]
        the_filenames_by_platform[ins_name.flutter] = [ins_name.flutter]
        the_filenames_by_platform[ins_name.swift] = [ins_name.swift]
        the_filenames_by_platform[ins_name.cocoapods] = [ins_name.cocoapods]
        cls.the_filenames_by_platform = the_filenames_by_platform

        the_prefixes_by_platform = dict()
        the_prefixes_by_platform[ins_name.gradle] = 'gradle'
        the_prefixes_by_platform[ins_name.package_json] = 'js'
        the_prefixes_by_platform[ins_name.roast] = 'roast'
        the_prefixes_by_platform[ins_name.go] = 'go'
        the_prefixes_by_platform[ins_name.flutter] = 'flutter'
        the_prefixes_by_platform[ins_name.swift] = 'https://github.com/swift'
        the_prefixes_by_platform[ins_name.cocoapods] = 'cocoa'
        cls.the_prefixes_by_platform = the_prefixes_by_platform

        the_expected_maxis_by_platform = dict()
        the_expected_maxis_by_platform[ins_name.gradle] = 10
        the_expected_maxis_by_platform[ins_name.package_json] = 6
        the_expected_maxis_by_platform[ins_name.roast] = 5
        the_expected_maxis_by_platform[ins_name.go] = 5
        the_expected_maxis_by_platform[ins_name.flutter] = 6 # with duplicated: +1
        the_expected_maxis_by_platform[ins_name.swift] = 7
        the_expected_maxis_by_platform[ins_name.cocoapods] = 3
        # 42
        cls.the_expected_maxis_by_platform = the_expected_maxis_by_platform

        the_expected_maxis_on_error_by_platform = dict()
        the_expected_maxis_on_error_by_platform[ins_name.gradle] = 1
        the_expected_maxis_on_error_by_platform[ins_name.package_json] = 2
        the_expected_maxis_on_error_by_platform[ins_name.roast] = 3
        the_expected_maxis_on_error_by_platform[ins_name.go] = 4 # with duplicated: +1
        the_expected_maxis_on_error_by_platform[ins_name.flutter] = 5
        the_expected_maxis_on_error_by_platform[ins_name.swift] = 6
        the_expected_maxis_on_error_by_platform[ins_name.cocoapods] = 7
        # 28
        cls.the_expected_maxis_on_error_by_platform = the_expected_maxis_on_error_by_platform

        a = CName().gradle
        b = CName().package_json
        c = CName().roast
        d = CName().go
        e = CName().flutter
        f = CName().swift
        g = CName().cocoapods
        cls.the_platforms = [a, b, c, d, e, f, g]

    def create_ins_filter(self, the_platforms, path_dependencies, path_licenses):
        ins_config = CConfig()
        ins_config.path_dependencies = path_dependencies
        ins_config.path_licenses = path_licenses
        ins_config.path_errors = path_licenses

        the_filenames = list()
        for platform in the_platforms:
            the_filenames += self.the_filenames_by_platform[platform]
        ins_config.the_filenames = the_filenames

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        return ins_filter

    def get_the_expected_dependencies(self, platform, maxi):
        the_expected_dependencies = list()

        prefix = self.the_prefixes_by_platform[platform]

        separator = '_'
        the_dependencies_with_underscore = [CName().package_json]
        if platform in the_dependencies_with_underscore:
            separator = '/'

        the_letters = list('abcdefghijklmnopqrstuvwxyz')
        for i in range(0, maxi):
            letter = the_letters[i]
            dependency = [prefix + separator + 'c' + separator+ letter]
            if platform == CName().gradle:
                dependency += [prefix + separator + 'n' + separator + letter]
            the_expected_dependencies.append(dependency)

        if platform == CName().package_json:
            dependencies = the_expected_dependencies[1]
            component = dependencies[0]
            component = '@' + component
            new_dependency = [component]
            the_expected_dependencies[1] = new_dependency

        if platform == CName().swift:
            dependencies = the_expected_dependencies[-1]
            component = dependencies[0]
            component = component.replace('https', 'http')
            new_dependency = [component]
            the_expected_dependencies[-1] = new_dependency

        return the_expected_dependencies

    def check_response(self, platform, response, the_expected, number_of_platforms):
        self.assertEqual(number_of_platforms, len(response.keys()), platform)

        the_dependencies = response[platform]
        self.assertEqual(len(the_expected), len(the_dependencies), platform)
        for expected in the_expected:
            msg = '\n platform: ' + platform + '\n ' + str(expected) + '\n in \n ' + str(the_dependencies)
            self.assertEqual(True, expected in the_dependencies, msg)

    def test_dependencies(self):
        for platform in self.the_platforms:
            ins_filter = self.create_ins_filter([platform], self.path_dependencies , self.path_no_file)
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            maxi = self.the_expected_maxis_by_platform[platform]
            the_expected = self.get_the_expected_dependencies(platform, maxi)
            self.check_response(platform, the_dependencies_by_platform, the_expected, 1)

    def test_dependencies_on_error(self):
        for platform in self.the_platforms:
            ins_filter = self.create_ins_filter([platform], self.path_no_file , self.path_dependencies_on_error)
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            maxi = self.the_expected_maxis_on_error_by_platform[platform]
            the_expected_on_error = self.get_the_expected_dependencies(platform, maxi)
            self.check_response(platform, the_dependencies_by_platform, the_expected_on_error, 1)

    @patch('sources.common.prompts.CPrompt.choose_the_data_to_treat')
    def test_choice_quit(self, mock_prompt):
        platform = CName().cocoapods
        the_platforms = [platform]
        ins_filter = self.create_ins_filter(the_platforms, self.path_dependencies , self.path_dependencies_on_error)
        mock_prompt.return_value = CChoice().quit
        the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
        self.assertEqual(None, the_dependencies_by_platform)

    @patch('sources.common.prompts.CPrompt.choose_the_data_to_treat')
    def test_choice_only_the_news(self, mock_prompt):
        platform = CName().cocoapods
        the_platforms = [platform]
        ins_filter = self.create_ins_filter(the_platforms, self.path_dependencies , self.path_dependencies_on_error)
        the_expected_dependencies = [['cocoa_c_a'], ['cocoa_c_b'], ['cocoa_c_c']]
        mock_prompt.return_value = CChoice().only_the_new_dependencies
        the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
        self.assertEqual(1, len(the_dependencies_by_platform.keys()))
        the_dependencies = the_dependencies_by_platform[platform]
        self.assertEqual(the_expected_dependencies[0], the_dependencies[0])
        self.assertEqual(the_expected_dependencies[1], the_dependencies[1])
        self.assertEqual(the_expected_dependencies[2], the_dependencies[2])

    @patch('sources.common.prompts.CPrompt.choose_the_data_to_treat')
    def test_choice_only_on_error(self, mock_prompt):
        platform = CName().cocoapods
        the_platforms = [platform]
        ins_filter = self.create_ins_filter(the_platforms, self.path_dependencies , self.path_dependencies_on_error)
        the_expected_dependencies = [['cocoa_c_a'], ['cocoa_c_b'], ['cocoa_c_c'], ['cocoa_c_d'], ['cocoa_c_e'], ['cocoa_c_f'], ['cocoa_c_g']]
        mock_prompt.return_value = CChoice().only_the_dependencies_on_error
        the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
        self.assertEqual(1, len(the_dependencies_by_platform.keys()))
        the_dependencies = the_dependencies_by_platform[platform]
        self.assertEqual(the_expected_dependencies[0], the_dependencies[0])
        self.assertEqual(the_expected_dependencies[1], the_dependencies[1])
        self.assertEqual(the_expected_dependencies[2], the_dependencies[2])
        self.assertEqual(the_expected_dependencies[3], the_dependencies[3])
        self.assertEqual(the_expected_dependencies[4], the_dependencies[4])
        self.assertEqual(the_expected_dependencies[5], the_dependencies[5])
        self.assertEqual(the_expected_dependencies[6], the_dependencies[6])
