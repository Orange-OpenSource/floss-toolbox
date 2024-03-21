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

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        path_tests = os.path.join(path_data, "get_the_dependencies")

        cls.path_no_file = os.path.join(path_tests, "no_file")
        cls.path_dependencies_empty = os.path.join(path_tests, "dependencies_empty")
        cls.path_dependencies = os.path.join(path_tests, "dependencies")
        cls.path_licenses = os.path.join(path_tests, "licenses")

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

        the_expected_by_platform = dict()
        the_expected_by_platform[ins_name.gradle] = 10
        the_expected_by_platform[ins_name.package_json] = 6
        the_expected_by_platform[ins_name.roast] = 5
        the_expected_by_platform[ins_name.go] = 5
        the_expected_by_platform[ins_name.flutter] = 6
        the_expected_by_platform[ins_name.swift] = 7
        the_expected_by_platform[ins_name.cocoapods] = 3
        cls.the_expected_by_platform = the_expected_by_platform

        the_expected_on_error_by_platform = dict()
        the_expected_on_error_by_platform[ins_name.gradle] = 1
        the_expected_on_error_by_platform[ins_name.package_json] = 2
        the_expected_on_error_by_platform[ins_name.roast] = 3
        the_expected_on_error_by_platform[ins_name.go] = 4 # with duplicated
        the_expected_on_error_by_platform[ins_name.flutter] = 5
        the_expected_on_error_by_platform[ins_name.swift] = 6
        the_expected_on_error_by_platform[ins_name.cocoapods] = 7
        cls.the_expected_on_error_by_platform = the_expected_on_error_by_platform

        the_prefixes_by_platform = dict()
        the_prefixes_by_platform[ins_name.gradle] = 'gradle'
        the_prefixes_by_platform[ins_name.package_json] = 'js'
        the_prefixes_by_platform[ins_name.roast] = 'roast'
        the_prefixes_by_platform[ins_name.go] = 'go'
        the_prefixes_by_platform[ins_name.flutter] = 'flutter'
        the_prefixes_by_platform[ins_name.swift] = 'https://github.com/swift'
        the_prefixes_by_platform[ins_name.cocoapods] = 'cocoa'
        cls.the_prefixes_by_platform = the_prefixes_by_platform

        cls.separator = '_'

    def get_the_expected_dependencies(self, prefix, separator, max):
        result = list()
        the_letters = list('abcdefghijklmnopqrstuvwxyz')
        for i in range(0, max):
            letter = the_letters[i]
            dependency = [prefix + separator + 'c' + separator+ letter]
            if 'gradle' in prefix:
                dependency += [prefix + separator + 'n' + separator + letter]
            result.append(dependency)
        return result

    def prepare_the_tests(self, path_dependencies, path_licenses, the_filenames):
        ins_config = CConfig()
        ins_config.path_dependencies = path_dependencies
        ins_config.path_errors = path_licenses
        ins_config.the_filenames = the_filenames
        ins_config.path_licenses = path_licenses

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        return ins_filter

    def check_response(self, the_dependencies_by_platform, the_expected_dependencies, platform, number_of_platforms):
        self.assertEqual(number_of_platforms, len(the_dependencies_by_platform.keys()), platform)

        the_dependencies = the_dependencies_by_platform[platform]
        self.assertEqual(len(the_expected_dependencies), len(the_dependencies), platform)
        for expected in the_expected_dependencies:
            msg = '\n platform: ' + platform + '\n ' + str(expected) + '\n in \n ' + str(the_dependencies)
            self.assertEqual(True, expected in the_dependencies, msg)


    def test_no_filename_in_config_ini(self):
        the_filenames = list()
        ins_filter = self.prepare_the_tests(self.path_dependencies, self.path_licenses, the_filenames)
        try:
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            self.fail()
        except Exception as e:
            self.assertEqual('No data to treat.', e.__str__())

    def test_no_path_dependencies_in_ini_file(self):
        the_filenames = 'build.gradle.kts'
        ins_filter = self.prepare_the_tests(str(), self.path_licenses, the_filenames)
        try:
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            self.fail()
        except Exception as e:
            msg = 'No data to treat.'
            self.assertEqual(msg, e.__str__())


    def test_path_dependencies_does_not_exist(self):
        the_filenames = 'build.gradle.kts'
        ins_filter = self.prepare_the_tests('bad path dependencies', self.path_licenses, the_filenames)
        try:
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            self.fail()
        except Exception as e:
            msg = 'No data to treat.'
            self.assertEqual(msg, e.__str__())


    def test_no_file_in_directory(self):
        the_filenames = self.the_filenames_by_platform['gradle']
        ins_filter = self.prepare_the_tests(self.path_no_file, self.path_licenses, the_filenames)
        try:
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            self.fail()
        except Exception as e:
            msg = 'No data to treat.'
            self.assertEqual(msg, e.__str__())


    def empty_file(self, platform):
        the_filenames = self.the_filenames_by_platform[platform][:]
        ins_filter = self.prepare_the_tests(self.path_dependencies_empty, self.path_licenses, the_filenames)
        try:
            the_dependencies_by_platform = CDependencies().get_the_dependencies(ins_filter)
            self.fail()
        except Exception as e:
            msg = 'No data to treat.'
            self.assertEqual(msg, e.__str__())

    def test_empty_file(self):
        platform = CName().gradle
        self.empty_file(platform)
        platform = CName().roast
        self.empty_file(platform)
        platform = CName().go
        self.empty_file(platform)
        platform = CName().cocoapods
        self.empty_file(platform)
        platform = CName().swift
        self.empty_file(platform)
        platform = CName().flutter
        self.empty_file(platform)
        platform = CName().package_json
        self.empty_file(platform)
