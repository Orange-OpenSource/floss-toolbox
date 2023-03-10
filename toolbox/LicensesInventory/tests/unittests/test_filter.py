# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
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
from sources.common import CFilter, CData, CName, CFile


class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup data for the tests
        """
        my_path = os.path.dirname(os.path.realpath(__file__))
        my_path_data = os.path.join(my_path, "data")
        cls.path_data = my_path_data

        cls.ins_filter = CFilter()
        cls.ins_data = CData()

        cls.instructions = 'implementation fileTree(dir: \'libs\', include: [\'*.jar\'])'

    def test_manage_the_comments(self):
        # simple comment
        the_lines = list()
        the_lines.append('a')
        i = 0
        last_position_of_the_comments = self.ins_filter.manage_the_comments(the_lines, i)
        self.assertEqual(-1, last_position_of_the_comments)

        the_lines.append('// simple comment')
        i += 1
        last_position_of_the_comments = self.ins_filter.manage_the_comments(the_lines, i)
        self.assertEqual(i, last_position_of_the_comments)

        the_lines += ['/*', 'complex comments', '*/']
        the_lines.append('b')
        i += 1
        last_position_of_the_comments = self.ins_filter.manage_the_comments(the_lines, i)
        i += 2
        self.assertEqual(i, last_position_of_the_comments)

    def test_delete_the_comments(self):
        # simple comment
        the_lines = list()
        the_lines.append('a')
        the_lines.append('// simple comment')
        the_lines.append('b')
        #mock_for_manage_the_comments.return_value = 1
        the_lines = self.ins_filter.delete_the_comments(the_lines)
        self.assertEqual(2, len(the_lines))
        self.assertEqual('a', the_lines[0])
        self.assertEqual('b', the_lines[1])

        the_lines = list()
        the_lines.append('a')
        the_lines.append('/*')
        the_lines.append('comments on')
        the_lines.append('severals lines')
        the_lines.append('*/')
        the_lines.append('b')
        #mock_for_manage_the_comments.return_value = 4
        the_lines = self.ins_filter.delete_the_comments(the_lines)
        self.assertEqual(2, len(the_lines))
        self.assertEqual('a', the_lines[0])
        self.assertEqual('b', the_lines[1])

    def test_clean(self):
        quote = self.ins_data.quote

        # line only with spaces
        the_lines = list()
        the_lines.append('  ')
        r = self.ins_filter.clean(the_lines, "")
        self.assertEqual(0, len(r))

        # spaces before and after
        the_lines = list()
        the_lines.append('  line ')
        r = self.ins_filter.clean(the_lines, "")
        self.assertEqual(1, len(r))
        self.assertEqual('line', r[0])

        # line with bad quote
        the_lines = list()
        the_lines.append(' \'line\' ')
        r = self.ins_filter.clean(the_lines, "")
        self.assertEqual(1, len(r))
        self.assertEqual(quote + 'line' + quote, r[0])

