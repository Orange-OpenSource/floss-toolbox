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
from sources.dependencies import CDependencies


class TestDependencies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")

        path_sources = os.path.join(path_data, "get_the_dependencies")
        cls.path_sources = path_sources

        cls.ins_name = CName()
        cls.ins_dependencies = CDependencies()

    def prepare_the_tests(self, sub_path_for_sources, filename):
        ins_config = CConfig()
        ins_config.path_dependencies = os.path.join(self.path_sources, sub_path_for_sources)
        ins_config.the_filenames = [filename]
        ins_config.path_licenses = self.path_sources
        ins_filter = CFilter()
        ins_filter.prepare(ins_config)

        return ins_filter

    def check_response(self, the_dependencies_by_platform, expected_dependencies, platform):
        self.assertEqual(1, len(the_dependencies_by_platform.keys()), platform)

        the_dependencies = the_dependencies_by_platform[platform]
        self.assertEqual(len(the_dependencies), len(expected_dependencies), platform)
        for the_values in expected_dependencies:
            msg = '\n platform: ' + platform + '\n ' + str(the_values) + '\n in \n ' + str(the_dependencies)
            self.assertEqual(True, the_values in the_dependencies, msg)

    def test_get_the_dependencies_for_flutter(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['component_a']
        b = ['component_b']
        c = ['component_c']
        d = ['component_d']
        e = ['component_e']
        f = ['f']
        expected_dependencies = [a, b, c, d, e, f]
        # test
        ins_filter = self.prepare_the_tests('simple', 'pubspec.yaml')
        the_dependencies_by_platform = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies_by_platform, expected_dependencies, self.ins_name.flutter)

    def test_get_the_dependencies_for_gradle(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['c_a', 'ns_a']
        b = ['c_b', 'ns_b']
        c = ['c_c', 'ns_c']
        expected_dependencies = [a, b, c]
        # test
        ins_filter = self.prepare_the_tests('simple', 'build.gradle')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.gradle)

        # test
        ins_filter = self.prepare_the_tests('simple', 'build.gradle.kts')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.gradle)

        # data/sources/complex/
        # the values in the dependencies
        a = ['c_a', 'ns_a']
        b = ['c_b', 'ns_b']
        c = ['c_c', 'ns_c']
        d = ['c_d', 'ns_d']
        expected_dependencies = [a, b, c, d]
        # test
        ins_filter = self.prepare_the_tests('complex', 'build.gradle')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.gradle)

    def test_get_the_dependencies_for_go(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['c_a']
        b = ['c_b']
        expected_dependencies = [a, b]
        # test
        ins_filter = self.prepare_the_tests('simple', 'go.mod')
        the_dependencies_by_platform = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies_by_platform, expected_dependencies, self.ins_name.go)

        # data/sources/complex/
        # the values in the dependencies
        a = ['c_a']
        b = ['c_b']
        c = ['c_c']
        expected_dependencies = [a, b, c]
        # test
        ins_filter = self.prepare_the_tests('complex', 'go.mod')
        the_dependencies_by_platform = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies_by_platform, expected_dependencies, self.ins_name.go)

    def test_get_the_dependencies_for_package_json(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['@c/a']
        b = ['c/b']
        c = ['c/c']
        d = ['c/d']
        e = ['c/e']
        expected_dependencies = [a, b, c, d, e]
        # test
        ins_filter = self.prepare_the_tests('simple', 'package.json')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.package_json)

        # data/sources/complex/
        # the values in the dependencies
        a = ['@c/a']
        b = ['c/b']
        c = ['c/c']
        d = ['c/d']
        e = ['c/e']
        expected_dependencies = [a, b, c, d, e]
        # test
        ins_filter = self.prepare_the_tests('complex', 'package.json')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.package_json)

    def test_get_the_dependencies_for_roast(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['c_a']
        b = ['c_b']
        expected_dependencies = [a, b]
        # test
        ins_filter = self.prepare_the_tests('simple', 'Cargo.lock')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.roast)

    def test_get_the_dependencies_for_swift(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['https://c_a']
        b = ['https://c_b']
        expected_dependencies = [a, b]
        # test
        ins_filter = self.prepare_the_tests('simple', 'Package.swift')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.swift)

        # data/sources/complex/
        # the values in the dependencies
        a = ['https://c_a']
        b = ['https://c_b']
        c = ['https://c_c']
        expected_dependencies = [a, b, c]
        # test
        ins_filter = self.prepare_the_tests('complex', 'Package.swift')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.swift)

    def test_get_the_dependencies_for_cocoa(self):
        # data/sources/simple/
        # the values in the dependencies
        a = ['CocoaAsyncSocket']
        b = ['DynamicCodable']
        c = ['Starscream']
        d = ['SwiftLint']
        e = ['OCast']
        # OCast is duplicated
        f = ['ReachabilitySwift']
        g = ['AppleReachability']
        expected_dependencies = [a, b, c, d, e, f, g]
        # test
        ins_filter = self.prepare_the_tests('simple', 'Podfile')
        the_dependencies = self.ins_dependencies.get_the_dependencies(ins_filter)
        self.check_response(the_dependencies, expected_dependencies, self.ins_name.cocoapods)

