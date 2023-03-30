#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        cls.path_data = path_data

    def test_configuration(self):
        ins_config = CConfig()
        ins_config.path = self.path_data
        ins_config.filename = 'config.ini'
        ins_config.get_the_config()

        expected = '/home/sub'
        self.assertEqual(expected, ins_config.path_dependencies)
        expected = ['f_a.ext', 'f_b.ext']
        self.assertEqual(expected, ins_config.the_filenames)
        expected = '/home/sub/licenses'
        self.assertEqual(expected, ins_config.path_licenses)
