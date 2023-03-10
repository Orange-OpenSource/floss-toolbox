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

from sources.common import CData, CName
from sources.search import CParsing


class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        my_path_data = os.path.join(my_path, "data")
        cls.path_data = my_path_data

        cls.ins_data = CData()
        cls.ins_parsing = CParsing()

    def test_extract_version_for_maven_central(self):
        #namespace = 'org.mockito'
        #component = 'mockito-core'

        folder = os.path.join(self.path_data, 'gradle')
        filename = 'version.json'
        file = os.path.join(folder, filename)
        r = self.ins_parsing.extract_version_for_maven_central(file)
        expected= '2.14.0-rc3'
        self.assertEqual(r, expected)

    def test_get_license_for_maven_central(self):
        #namespace = 'org.mockito'
        #component = 'mockito-core'
        #version = '2.14.0-rc3'

        folder = os.path.join(self.path_data, 'gradle')
        filename = 'license_maven_central.pom'
        file = os.path.join(folder, filename)
        r = self.ins_parsing.get_license_for_maven_central(file)
        expected_name = 'mockito-core'
        name = r[0]
        self.assertEqual(expected_name, name)
        expected_license = 'The MIT License'
        license = r[1]
        self.assertEqual(expected_license, license)

    def test_get_license_for_github(self):
        #component = 'appcompat'
        #namespace = 'androidx.appcompat'

        folder = os.path.join(self.path_data, 'gradle')
        filename = 'license_github.json'
        file = os.path.join(folder, filename)
        r = self.ins_parsing.get_license_for_github(file)

        expected_name = 'AppCompat-Extension-Library'
        name = r[0]
        self.assertEqual(expected_name, name)

        expected_license = 'Apache License 2.0'
        license = r[1]
        self.assertEqual(expected_license, license)

    def test_get_license_for_package_json(self):
        #component = 'popperjs/core'

        folder = os.path.join(self.path_data, 'package_json')
        filename = 'license_package_json.html'
        file = os.path.join(folder, filename)
        r = self.ins_parsing.get_license_for_package_json(file)

        expected_license = 'MIT'
        license = r[0]
        self.assertEqual(expected_license, license)

    def test_get_license_for_roast(self):
        #component = 'adler32'

        folder = os.path.join(self.path_data, 'roast')
        filename = 'license_roast.json'
        file = os.path.join(folder, filename)
        r = self.ins_parsing.get_license_for_roast(file)

        expected_license = 'Zlib'
        license = r[0]
        self.assertEqual(expected_license, license)


