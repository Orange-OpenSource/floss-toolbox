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


import json 


class CData:

    def __init__(self):
        self.the_letters = self.get_the_letters()
        self.the_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.old_quote = '\''
        self.quote = '\"'
        self.the_comments = ['//', '/*', '*/']
        self.head = '{'
        self.foot = '}'

    def get_the_letters(self):
        the_lowers = list()
        the_uppers = list()
        for ascii_code in range(97, 123):
            character = chr(ascii_code)
            the_lowers.append(character)
            the_uppers.append(character.upper())

        return (the_lowers + the_uppers)
