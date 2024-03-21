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


from sources.common import CChoice
ins_choice = CChoice()


class CPrompt:

    def choose_the_data_to_treat(self):
        choice = None

        response = None
        new_line = '\n'
        line = 'Do you want to treat the dependencies on error or the new dependencies ?' + new_line
        indent = '\t'
        the_lines = indent + 'n (the new dependencies)' + new_line
        the_lines += indent + 'e (the dependencies on error)' + new_line
        the_lines += indent + 'q (quit the program)' + new_line
        the_lines += 'your choice: '
        the_responses = ['q', 'e', 'n']
        while response not in the_responses:
            r = input(the_lines)
            response = r.lower()

        if response == 'q':
            choice = ins_choice.quit
        elif response == 'n':
            choice = ins_choice.only_the_new_dependencies
        elif response == 'e':
            choice = ins_choice.only_the_dependencies_on_error

        return choice
