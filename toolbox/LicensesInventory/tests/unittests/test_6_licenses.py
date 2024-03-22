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

import sys
import os

from sources.common import CFilter, CName
from sources.configuration import CConfig
from sources.search import CSearch


class TestLicenses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # for go_github: no data to treat this case
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")
        path_tests = os.path.join(path_data, "get_the_licenses")

        path_sources = os.path.join(path_tests, "sources")
        cls.path_sources = path_sources

        path_results = os.path.join(path_tests, "results")
        cls.path_results = path_results

    def get_dependency_and_license_for_test_ok(self, platform):
        dependency = None
        license = None

        ins_name = CName()
        if platform == ins_name.cocoapods:
            dependency = ['AppleReachability']
            license = ['AppleReachability is available under the Apple license. See the LICENSE.txt file for more info.']
        elif platform == CName().swift:
            dependency = ['https://github.com/AliSoftware/OHHTTPStubs']
            license = ['This project and library has been created by Olivier Halligon (@aligatr on Twitter) and is under the MIT License.']
        elif platform == CName().flutter:
            dependency = ['build_runner']
            license = ['BSD-3-Clause (LICENSE)']
        elif platform == CName().go:
            dependency = ['emperror.dev/errors']
            license = ['The MIT License (MIT). Please see License File for more information.']
        elif platform == CName().package_json:
            dependency = ['@babel/core']
            license = ['MIT']
        elif platform == CName().gradle:
            component = 'androidannotations'
            namespace = 'org.androidannotations'
            dependency = [component, namespace]
            name = 'androidannotations'
            result = 'Other'
            license = [name, result]
        elif platform == CName().roast:
            dependency = ['adler']
            license = ['0BSD OR MIT OR Apache-2.0']

        return (dependency, license)

    def get_path_platform(self, platform):
        path_platform = None

        ins_name = CName()

        if platform == ins_name.cocoapods:
            path_platform = 'Podfile'
        if platform == ins_name.swift:
            path_platform = 'package_swift'
        if platform == ins_name.flutter:
            path_platform = 'pubspec_yaml'
        if platform == ins_name.gradle:
            path_platform = 'gradle'
        if platform == ins_name.package_json:
            path_platform = 'package_json'
        if platform == ins_name.roast:
            path_platform = 'cargo_lock'
        if platform == ins_name.go:
            path_platform = 'go_mod'

        return path_platform

    def get_file_for_mock(self, platform, dependency):
        ins_name = CName()
        if platform == ins_name.cocoapods:
            filename = dependency[0] + '.html'
        elif platform == CName().swift:
            component = dependency[0]
            component = component.replace('https://github.com/', str())
            component = component.replace('/', '_')
            filename = component + '.html'
        elif platform == CName().flutter:
            filename = dependency[0] + '.html'
        elif platform == CName().go:
            component = dependency[0]
            component = component.replace('/', '_')
            filename = component + '.html'
        elif platform == CName().package_json:
            component = dependency[0]
            component = component.replace('/', '_')
            filename = component + '.html'
        elif platform == CName().gradle:
            filename = dependency[0]
            if len(dependency) == 2:
                filename += '__' + dependency[1]
            filename = filename.replace('.', '_')
            filename += '_github.json'            
        elif platform == CName().roast:
            filename = dependency[0] + '.json'

        path_platform = self.get_path_platform(platform)
        path = os.path.join(self.path_results, path_platform)
        file = os.path.join(path, filename)

        return file

    def mock_ins_search(self, platform, dependency, error_code):
        ins_search = CSearch()
        ins_search.ins_download = MagicMock()
        ins_search.ins_download.error_code = error_code
        file = self.get_file_for_mock(platform, dependency)
        ins_search.ins_download.get_file.return_value = file

        return ins_search

    def prepare(self, platform, dependency):
        ins_config = CConfig()
        ins_config.path_licenses = self.path_results

        the_dependencies = [dependency]
        the_dependencies_by_platform = dict()
        the_dependencies_by_platform[platform] = the_dependencies

        return (ins_config, the_dependencies_by_platform)

    def check_result(self, platform, expected, the_licenses):
            the_dependencies = the_licenses[platform]
            self.assertEqual(1, len(the_dependencies), platform)
            dependency = the_dependencies[0]
            self.assertEqual(len(expected), len(dependency), platform)
            for i in range(0, len(expected)):
                self.assertEqual(expected[i], dependency[i], platform)

    def test_error_code(self):
        platform = CName().cocoapods
        dependency = ['ReachabilitySwift']
        license = None # unused
        r = self.prepare(platform, dependency)
        ins_config, the_dependencies_by_platform = r

        error_code = '300'
        ins_search = self.mock_ins_search(platform, dependency, error_code)
        r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, None)
        the_licenses, the_errors = r

        self.assertEqual(0, len(the_licenses))
        expected = ['error code = 300'] + dependency
        self.check_result(platform, expected, the_errors)

    def test_ok(self):
        a = CName().cocoapods
        b = CName().swift
        c = CName().flutter
        d = CName().go
        e = CName().package_json
        f= CName().gradle
        g = CName().roast

        the_platforms = [a, b, c, d, e, f, g]
        for platform in the_platforms:
            r = self.get_dependency_and_license_for_test_ok(platform)
            dependency, license = r
            r = self.prepare(platform, dependency)
            ins_config, the_dependencies_by_platform = r
            error_code = '200'
            ins_search = self.mock_ins_search(platform, dependency, error_code)
            r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, None)
            the_licenses, the_errors = r

            expected = dependency + license
            self.check_result(platform, expected, the_licenses)

    def test_no_head_in_downloaded_file(self):
        platform = CName().cocoapods
        dependency = ['ReachabilitySwift']
        license = [str()]

        r = self.prepare(platform, dependency)
        ins_config, the_dependencies_by_platform = r

        error_code = '200'
        #filename = dependency[0] + '.html'
        ins_search = self.mock_ins_search(platform, dependency, error_code)

        r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, None)
        the_licenses, the_errors = r

        expected = dependency
        self.check_result(platform, expected, the_licenses)

    def test_gradle_with_no_namespace(self):
        platform = CName().gradle
        dependency = ['appcompat']
        name = 'appcompatprocessor'
        result = 'Apache License 2.0'
        license = [name, result]

        r = self.prepare(platform, dependency)
        ins_config, the_dependencies_by_platform = r

        error_code = '200'
        #filename = dependency[0]
        #filename = filename.replace('.', '_')
        #filename += '_github.json'            
        ins_search = self.mock_ins_search(platform, dependency, error_code)

        r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, None)
        the_licenses, the_errors = r

        expected = dependency + license
        self.check_result(platform, expected, the_licenses)

    def test_go_github(self):
        platform = CName().go
        dependency = ['github.com/antihax/optional']
        name = ''
        result = 'MIT license'
        license = [result]

        r = self.prepare(platform, dependency)
        ins_config, the_dependencies_by_platform = r

        error_code = '200'
        ins_search = self.mock_ins_search(platform, dependency, error_code)

        r = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, None)
        the_licenses, the_errors = r

        expected = dependency + license
        self.check_result(platform, expected, the_licenses)
