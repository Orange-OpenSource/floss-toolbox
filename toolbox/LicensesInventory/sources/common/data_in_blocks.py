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


class CDataInBlock:

    def __init__(self, the_heads, the_foot):
        self.the_heads = the_heads
        self.the_foot = the_foot

    def get(self, the_lines, ends_by_feet, data_with_head):
        result = list()

        level = 0
        for line in the_lines:
            if level < 0: level = 0

            # feet
            if line.strip() in self.the_foot:
                if ends_by_feet == True:
                    level = 0
                else:
                    level = level -1
                continue

            # head
            if line.strip() in self.the_heads:
                level = level +1
                continue

            if data_with_head == True and level > 0:
                my_line = line.strip()
                if len(my_line) > 1:
                    v = line.strip()[-1]
                    if v == '{':
                        level += 1
                        continue

            if (level > 0) and (line.strip() != str()):
                result.append(line)

        return result
