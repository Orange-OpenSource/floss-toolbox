#!/usr/bin/env python3
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
        cls.ins_search = CSearch()

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

    def check_response(self, the_licenses_by_platform, expected, platform):
        self.assertEqual(1, len(the_licenses_by_platform))
        the_licenses = the_licenses_by_platform[platform]
        self.assertEqual(expected, the_licenses[0], platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_flutter(self, mock_check_the_directory, mock_get_file, mock_stdout):
        platform = self.ins_name.flutter
        filename_dependencies = 'pubspec.yaml'
        dependency = ['build_runner']
        filename_licenses = 'build_runner.html'
        path_platform = 'pubspec_yaml'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'BSD-3-Clause'
        expected = dependency + [license]

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_gradle(self, mock_check_the_directory, mock_get_file, mock_stdout):
        platform = self.ins_name.gradle
        filename_dependencies = 'build.gradle'
        component = 'appcompat'
        namespace = 'androidx.appcompat'
        dependency = [component, namespace]
        filename_licenses = component + '_github.json'
        path_platform = 'gradle'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'Apache License 2.0'
        name = 'appcompatprocessor'
        expected = dependency + [name, license]

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_package_json(self, mock_check_the_directory, mock_get_file, mock_stdout):
        platform = self.ins_name.package_json
        filename_dependencies = 'package.json'
        component = '@babel/core'
        dependency = [component]
        c = component.replace('/', '_')
        filename_licenses = c + '.html'
        path_platform = 'package_json'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'MIT'
        expected = [component, license]

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_roast(self, mock_check_the_directory, mock_get_file, mock_stdout):
        platform = self.ins_name.roast
        filename_dependencies = 'Cargo.lock'
        component = 'adler'
        dependency = [component]
        filename_licenses = component + '.json'
        path_platform = 'cargo_lock'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = '0BSD OR MIT OR Apache-2.0'
        expected = [component, license]

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_go(self, mock_check_the_directory, mock_get_file, mock_stdout):
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

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_swift(self, mock_check_the_directory, mock_get_file, mock_stdout):
        platform = self.ins_name.swift
        filename_dependencies = 'Package.swift'
        component = 'https://github.com/AliSoftware/OHHTTPStubs'
        dependency = [component]
        c = component.replace('https://github.com/', str())
        c = c.replace('/', '_')
        filename_licenses = c + '.html'
        path_platform = 'package_swift'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'MIT license'
        expected = [component, license]

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)

    @patch('sys.stdout')
    @patch('sources.search.CDownload.get_file')
    @patch('sources.search.downloads.CFile.check_the_directory')
    def test_get_the_licenses_for_cocoa(self, mock_check_the_directory, mock_get_file, mock_stdout):
        platform = self.ins_name.cocoapods
        filename_dependencies = 'Podfile'
        component = 'SwiftLint'
        dependency = [component]
        filename_licenses = component + '.html'
        path_platform = 'Podfile'

        r = self.prepare_the_tests(filename_dependencies, platform, dependency, path_platform, filename_licenses)
        the_dependencies_by_platform, ins_config, ins_filter, file = r
        mock_get_file.return_value = file

        license = 'MIT'
        expected = [component, license]

        the_licenses_by_platform = self.ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)
        self.check_response(the_licenses_by_platform, expected, platform)
