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


class CComment:

    def __init__(self):
        self.the_simples = ['#', '//']
        self.the_complexes = [('/*', '*/')]

    def is_simple_comment(self, ref):
        line = ref.strip()
        for start in self.the_simples:
            if line.find(start) == 0:
                return True

                return False

    def is_complex_comment(self, the_lines, a):
        line = the_lines[a].replace('\n', str())
        b = a + 0

        # search comment
        the_values = tuple()
        my_line = line.strip()
        for start_and_stop in self.the_complexes:
            start, stop = start_and_stop
            p = my_line.find(start)
            if p > -1:
                the_values = (start, stop, p)

        if the_values == tuple():
            return (line, a)

        text_before = str()
        if p > 0:
            text_before = line[0:p]
            my_line = my_line[p:]

        # search the end of the comment
        b = a + 0
        while stop not in my_line:
            b += 1
            my_line = the_lines[b].replace('\n', str())

        text_after = str()
        p_stop = my_line.find(stop)
        p_stop += len(stop)
        if p_stop < len(my_line):
            text_after = my_line[p:]

        text_after = text_after.strip()
        if (text_before == str()) and (text_after == str()):
            line = None
        else:
            line = text_before + ' ' + text_after
            line = line.rstrip()

        return (line, b)

    def delete(self, the_lines):
        result = list()

        to_continue = False
        a = -1
        while (a+1) < len(the_lines):
            a += 1
            line = the_lines[a].replace('\n', str())
            to_continue = True

            if self.is_simple_comment(line) == True:
                to_continue = False

            if to_continue == True:
                r = self.is_complex_comment(the_lines, a)
                line, a = r
                if line == None:
                    to_continue = False

            if to_continue == True:
                result.append(line)

        return result
