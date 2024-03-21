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

import os

from sources.common import CFile, CFileException


class CConfig():

    def __init__(self):
        self.path = os.getcwd()
        self.filename = "config.ini"

        self.path_dependencies = str()
        self.the_filenames = list()
        self.path_licenses = str()
        self.number_of_errors_max = 999

        self.filename_for_the_licenses = 'licenses_[platform].txt'
        self.path_errors = str()
        self.model_for_errors_file = 'errors_[platform].txt'

        self.separator = ' = '

    def extract_data_from_ini_file(self, the_lines):

        for i in range(len(the_lines) - 1, -1, -1):
            line = the_lines[i]
            if self.separator not in line: continue

            the_parameters = line.split(self.separator)
            options = the_parameters[0]
            value = the_parameters[1]
            value = value.strip()

            if "parse" in options:
                self.path_dependencies = value
            elif "file" in options:
                if value != str():
                    self.the_filenames = value.split(", ")
            elif "license" in options:
                self.path_licenses = value
            elif "errors" in options:
                self.number_of_errors_max = value

    def get_the_config(self):

        ins_file = CFile()
        try:
            the_lines = ins_file.read_text_file (self.path, self.filename)
        except Exception as e:
            raise Exception(e.__str__())
        self.extract_data_from_ini_file(the_lines)
        self.path_errors = self.path_licenses

    def str(self):
        print('Path to parse the dependencies:')
        print(self.path_dependencies)
        print()

        print('The filenames to parse:')
        for filename in self.the_filenames:
            my_filename = '\t' + filename
            print(my_filename)
        print()

        print('Path to store the licenses:')
        print(self.path_licenses)
        print()

