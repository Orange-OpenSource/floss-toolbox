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
from sources.search import CSearch


class TestLicenses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        path_tests = os.path.join(path_data, "get_the_licenses")

        path_sources = os.path.join(path_tests, "sources")
        cls.path_sources = path_sources

        path_results = os.path.join(path_tests, "results")
        cls.path_results = path_results

        cls.ins_name = CName()
        ins_search = CSearch()
        ins_search.ins_download.error_code = '200'
        cls.ins_search = ins_search

    def prepare_the_tests(self, filename_dependencies, platform, dependency, path_platform, filename_licenses):
        ins_config = CConfig()
        ins_config.path_dependencies = self.path_sources
        ins_config.the_filenames = [filename_dependencies]
        ins_config.path_licenses = self.path_results

        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        the_dependencies = [dependency]
        the_dependencies_by_platform = dict()
        the_dependencies_by_platform[platform] = the_dependencies

        path = os.path.join(self.path_results, path_platform)
        file = os.path.join(path, filename_licenses)

        return (the_dependencies_by_platform, ins_config, ins_filter, file)

    def check_response(self, the_licenses_by_platform, expected, platform, number_of_values):
        self.assertEqual(1, len(the_licenses_by_platform))
        the_licenses = the_licenses_by_platform[platform]
        #license and expected
        license = the_licenses[0]
        self.assertEqual(number_of_values, len(license))

        for i in range(0, len(license)):
            self.assertEqual(expected[i], license[i], platform)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_flutter(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.flutter
        filename_dependencies = 'pubspec.yaml'
        dependency = ['build_runner']
        filename_licenses = 'build_runner.html'
        path_platform = 'pubspec_yaml'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        self.ins_search.ins_download.error_code = '200'
        license = 'BSD-3-Clause (LICENSE)'
        expected = dependency + [license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_gradle(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.gradle
        filename_dependencies = 'build.gradle'
        path_platform = 'gradle'

        #component 1
        component = 'appcompat'
        namespace = 'androidx.appcompat'
        dependency = [component, namespace]
        filename_licenses = component + '_github.json'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        self.ins_search.ins_download.error_code = '200'
        license = 'Apache License 2.0'
        name = 'appcompatprocessor'
        expected = dependency + [name, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 4
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

        #component 2
        component = 'androidannotations'
        namespace = 'org.androidannotations'
        dependency = [component, namespace]
        filename_licenses = component + '_github.json'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        self.ins_search.ins_download.error_code = '200'
        name = 'androidannotations'
        license = 'Other'
        expected = dependency + [name, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 4
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_gradle_on_error(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.gradle
        filename_dependencies = 'build.gradle'
        component = 'appcompat'
        namespace = 'androidx.appcompat'
        dependency = [component, namespace]
        filename_licenses = component + '_github.json'
        path_platform = 'gradle'

        #error 300
        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = None

        error_code = '300'
        self.ins_search.ins_download.error_code = error_code
        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r

        self.assertEqual([platform], list(the_licenses_by_platform.keys()))
        the_licenses = the_licenses_by_platform[platform]
        self.assertEqual(1, len(the_licenses))
        license = the_licenses[0]
        self.assertEqual(dependency[0], license[0])
        self.assertEqual(dependency[1], license[1])
        expected = 'error code=' + str(error_code)
        self.assertEqual(expected, license[2])

        self.assertEqual(0, len(on_error))

        #error 403
        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = None

        error_code = '403'
        self.ins_search.ins_download.error_code = error_code
        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r

        self.assertEqual([platform], list(the_licenses_by_platform.keys()))
        the_licenses = the_licenses_by_platform[platform]
        self.assertEqual(0, len(the_licenses))

        self.assertEqual(1, len(on_error[platform]))
        self.assertEqual(on_error[platform][0], dependency)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_package_json(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.package_json
        filename_dependencies = 'package.json'
        path_platform = 'package_json'

        component = '@babel/core'
        dependency = [component]
        c = component.replace('/', '_')
        filename_licenses = c + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        self.ins_search.ins_download.error_code = '200'
        license = 'MIT'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)
        #the_licenses = the_licenses_by_platform[platform]
        #license and expected
        #license = the_licenses[0]
        #self.assertEqual(number_of_values, len(license))
        #self.assertEqual(0, 8)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_roast(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.roast
        filename_dependencies = 'Cargo.lock'
        component = 'adler'
        dependency = [component]
        filename_licenses = component + '.json'
        path_platform = 'cargo_lock'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        self.ins_search.ins_download.error_code = '200'
        license = '0BSD OR MIT OR Apache-2.0'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_go(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.go
        filename_dependencies = 'go.mod'
        component = 'emperror.dev/errors'
        dependency = [component]
        c = component.replace('/', '_')
        filename_licenses = c + '.html'
        path_platform = 'go_mod'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'MIT'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_swift(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.swift
        filename_dependencies = 'Package.swift'
        path_platform = 'package_swift'

        #component 1
        component = 'https://github.com/AliSoftware/OHHTTPStubs'
        dependency = [component]
        c = component.replace('https://github.com/', str())
        c = c.replace('/', '_')
        filename_licenses = c + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'This project and library has been created by Olivier Halligon (@aligatr on Twitter) and is under the MIT License.'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

        #component 2
        component = 'https://github.com/CocoaLumberjack/CocoaLumberjack.git'
        dependency = [component]
        c = component.replace('https://github.com/', str())
        c = c.replace('/', '_')
        c = c.replace('.git', '_git')
        filename_licenses = c + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'CocoaLumberjack is available under the BSD 3 license. See the LICENSE file. BSD-3-Clause license'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

        #component 3
        component = 'https://github.com/apple/swift-collections'
        dependency = [component]
        c = component.replace('https://github.com/', str())
        c = c.replace('/', '_')
        c = c.replace('-', '_')
        filename_licenses = c + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'Apache-2.0 license'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

        #component 4
        component = 'https://github.com/krzyzanowskim/CryptoSwift.git'
        dependency = [component]
        c = component.replace('https://github.com/', str())
        c = c.replace('/', '_')
        c = c.replace('.git', '_git')
        filename_licenses = c + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'Copyright (C) 2014-2022 Marcin Krzyanowski marcin@krzyzanowskim.comThis software is provided \'as-is\', without any express or implied warranty. View license'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_cocoa(self, mock_check_the_directory, mock_get_file):
        platform = self.ins_name.cocoapods
        filename_dependencies = 'Podfile'
        path_platform = 'Podfile'

        #component 1:
        component = 'SwiftLint'
        dependency = [component]
        filename_licenses = component + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'MIT'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

        #component 2:
        component = 'AppleReachability'
        dependency = [component]
        filename_licenses = component + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'AppleReachability is available under the Apple license. See the LICENSE.txt file for more info.'
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)

        #component 3: no head with "license" or "License", etc
        component = 'ReachabilitySwift'
        dependency = [component]
        filename_licenses = component + '.html'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = None
        expected = [component, license]

        r = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        the_licenses_by_platform, on_error = r
        number_of_values = 2
        self.check_response(the_licenses_by_platform, expected, platform, number_of_values)
