# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import unittest
from unittest.mock import Mock, MagicMock, patch
from unittest.mock import call
import os

from sources.configuration import CConfig
from sources.common import CData, CName
from sources.dependencies import CParsing

class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        my_path_data = os.path.join(my_path, "data")
        cls.path_data = my_path_data

        cls.ins_data = CData()
        cls.ins_parsing = CParsing()

    def test_get_data(self):
        ins_parsing = CParsing()
        ins_data = CData()

        quote = ins_data.quote
        h_a = quote + 'peerDependencies' + quote + ': {'
        h_b = quote + 'devDependencies' + quote + ': {'
        h_c = quote + 'dependencies' + quote + ': {'
        ins_parsing.the_heads = [h_a, h_b, h_c]

        foot = '}'
        comma = ','
        ins_parsing.the_foots = [foot, foot + comma]

        # no head, no foot
        the_lines = list()
        the_lines.append('text before')
        the_lines.append('text after')
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(0, len(result))

        # head + foot
        the_lines = list()
        the_lines.append('text before')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('text after')
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(0, len(result))

        # head + value + foot
        the_lines = list()
        the_lines.append('text before')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('line_a')
        the_lines.append('head and foot between quotes \"{}\"')
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('text after')
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(2, len(result))

        # head + value + head + foot + value + foot
        the_lines = list()
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('before sub')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('after sub')
        the_lines.append(ins_parsing.the_foots[0])
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(2, len(result))

        # head + value + head + value + foot and comma + value + foot
        the_lines = list()
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('before sub')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('value in sub')
        the_lines.append(ins_parsing.the_foots[1])
        the_lines.append('after sub')
        the_lines.append(ins_parsing.the_foots[0])
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(3, len(result))

        # head + value + head + value + foot + value + foot
        the_lines = list()
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('before sub')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('line in sub')
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('after sub')
        the_lines.append(ins_parsing.the_foots[0])
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(3, len(result))

        # head + value + head + foot + value + foot
        the_lines = list()
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('before sub')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('after sub')
        the_lines.append(ins_parsing.the_foots[0])
        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(2, len(result))

    def test_get_data_all(self):
        ins_parsing = CParsing()
        ins_data = CData()

        quote = ins_data.quote
        h_a = quote + 'peerDependencies' + quote + ': {'
        h_b = quote + 'devDependencies' + quote + ': {'
        h_c = quote + 'dependencies' + quote + ': {'
        ins_parsing.the_heads = [h_a, h_b, h_c]

        foot = '}'
        comma = ','
        ins_parsing.the_foots = [foot, foot + comma]

        # head + value + value + head + value + value + foot + value + value + foot
        the_lines = list()
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('text before head {')
        the_lines.append('exclude data')
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('a before sub')
        the_lines.append(ins_parsing.the_heads[0])
        the_lines.append('b in sub')
        the_lines.append('c in sub')
        the_lines.append(ins_parsing.the_foots[0])
        the_lines.append('d after sub')
        the_lines.append('e after sub')
        the_lines.append(ins_parsing.the_foots[0])

        ins_parsing.the_lines = the_lines
        r = ins_parsing.get_data(0, 1)
        result, i = r
        self.assertEqual(6, len(result))

    def test_manage_gradle(self):
        bad = list()
        ins_data = CData()
        quote = ins_data.quote

        # the line begins with 'exclude'
        the_lines = list()
        the_lines.append('exclude dddd')
        r = self.ins_parsing.manage_gradle(the_lines)
        self.assertEqual(bad, r)

        # string and head
        the_lines = list()
        the_lines.append('unknown ' + ins_data.head)
        r = self.ins_parsing.manage_gradle(the_lines)
        self.assertEqual(bad, r)

        # good line and head
        the_lines = list()
        the_lines.append('prefix ' + quote + 'n:c:v' + quote + ' ' + self.ins_data.head)
        r = self.ins_parsing.manage_gradle(the_lines)
        self.assertEqual(bad, r)

        # bad line
        the_lines = list()
        line = 'api project(' + quote + ':lib' + quote + ')'
        the_lines.append(line)
        r = self.ins_parsing.manage_gradle(the_lines)
        self.assertEqual(bad, r)

        # good line
        the_lines = list()
        line = 'prefix ' + quote + 'n:c:v' + quote
        the_lines.append(line)
        r = self.ins_parsing.manage_gradle(the_lines)
        self.assertEqual(1, len(r))
        the_values = r[0]
        self.assertEqual('c', the_values[0])
        self.assertEqual('n', the_values[1])

    def test_manage_package_json(self):
        ins_data = CData()
        quote = ins_data.quote
        good = 'component'
        bad = list()
        separator = ' : '

        # component: first quote: no
        the_lines = list()
        line = 'component' + quote + separator + quote + 'version' + quote
        the_lines.append(line)
        r = self.ins_parsing.manage_package_json(the_lines)
        self.assertEqual(bad, r)

        # component: second quote: no
        the_lines = list()
        line = quote + 'component' + separator + quote + 'version' + quote
        the_lines.append(line)
        r = self.ins_parsing.manage_package_json(the_lines)
        self.assertEqual(bad, r)

        # version: first quote: no
        the_lines = list()
        line = quote + 'component' + quote + separator + 'version' + quote
        the_lines.append(line)
        r = self.ins_parsing.manage_package_json(the_lines)
        self.assertEqual(1, len(r))
        the_values = r[0]
        self.assertEqual('component', the_values[0])

        # version: second quote: no
        the_lines = list()
        line = quote + 'component' + quote + separator + quote + 'version'
        the_lines.append(line)
        r = self.ins_parsing.manage_package_json(the_lines)
        self.assertEqual(1, len(r))
        the_values = r[0]
        self.assertEqual('component', the_values[0])

        # good line
        the_lines = list()
        line = quote + 'component' + quote + separator + quote + 'version' + quote
        the_lines.append(line)
        r = self.ins_parsing.manage_package_json(the_lines)
        self.assertEqual(1, len(r))
        the_values = r[0]
        self.assertEqual('component', the_values[0])

    def test_get_data_for_roast(self):
        the_lines = list()
        the_lines.append('[[package]]')
        the_lines.append('name = c_a')
        the_lines.append('a = aa')
        the_lines.append('b = bb')
        the_lines.append('')

        r = self.ins_parsing.get_data_for_each_block(the_lines)
        self.assertEqual(1, len(r))
        the_values = r[0]
        self.assertEqual('c_a', the_values[0])

        # with severals blocks
        the_lines.append('[[package]]')
        the_lines.append('name = c_b')
        the_lines.append('a = aa')
        the_lines.append('b = bb')
        the_lines.append('')

        r = self.ins_parsing.get_data_for_each_block(the_lines)
        self.assertEqual(2, len(r))

        the_values = r[0]
        self.assertEqual('c_a', the_values[0])

        the_values = r[1]
        self.assertEqual('c_b', the_values[0])
