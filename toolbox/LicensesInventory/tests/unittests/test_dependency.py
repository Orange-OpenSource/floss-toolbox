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

from sources.dependencies import CDependencies
class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup data for the tests
        """
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")

        the_files = list()
        file_a = os.path.join(path_data, 'dependency_a.txt')
        the_files.append(file_a)
        file_b = os.path.join(path_data, 'dependency_b.txt')
        the_files.append(file_b)
        cls.the_files = the_files

        #cls.path_data = path_data

        cls.instance = CDependencies()

    def test_delete_the_duplicated_1_value(self):
        ins_dependency = CDependencies()
        platform = 'gradle'

        the_dependencies_by_language = dict()
        the_dependencies = list()
        dependency_a = ['c_a']
        the_dependencies.append(dependency_a)
        dependency_b = ['c_b']
        the_dependencies.append(dependency_b)
        the_dependencies.append(dependency_b)

        the_dependencies_by_language[platform] = the_dependencies

        r = ins_dependency.delete_the_duplicated(the_dependencies_by_language)

        the_dependencies = r[platform]
        self.assertEqual(2, len(the_dependencies))
        dependency = the_dependencies[0]
        self.assertEqual(1, len(dependency))
        self.assertEqual('c_a', dependency[0])
        dependency = the_dependencies[1]
        self.assertEqual(1, len(dependency))
        self.assertEqual('c_b', dependency[0])

    def test_delete_the_duplicated_2_values(self):
        ins_dependency = CDependencies()
        platform = 'gradle'

        the_dependencies_by_language = dict()
        the_dependencies = list()
        dependency_a = ['c_a', 'n_a']
        the_dependencies.append(dependency_a)
        dependency_b = ['c_b', 'n_b']
        the_dependencies.append(dependency_b)
        the_dependencies.append(dependency_b)

        the_dependencies_by_language[platform] = the_dependencies

        r = ins_dependency.delete_the_duplicated(the_dependencies_by_language)

        the_dependencies = r[platform]
        self.assertEqual(2, len(the_dependencies))
        dependency = the_dependencies[0]
        self.assertEqual(2, len(dependency))
        self.assertEqual('c_a', dependency[0])
        self.assertEqual('n_a', dependency[1])
        dependency = the_dependencies[1]
        self.assertEqual(2, len(dependency))
        self.assertEqual('c_b', dependency[0])
        self.assertEqual('n_b', dependency[1])


