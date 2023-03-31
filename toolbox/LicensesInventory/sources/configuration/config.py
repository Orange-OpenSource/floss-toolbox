#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

import os

from ..common import CFile, CName


def value_is_empty(value):
    if value == '' or value == None:
        return True
    return False

class CConfig():

    def __init__(self):
        self.path = os.getcwd()
        self.filename = "config.ini"
        self.separator = ' = '
        self.path_dependencies = str()
        self.the_filenames = list()
        self.path_licenses = str()

    def extract_data_from_ini_file(self, the_lines):

        for i in range(len(the_lines) - 1, -1, -1):
            line = the_lines[i]
            if self.separator in line:
                the_parameters = line.split(self.separator)
                options = the_parameters[0]
                value = the_parameters[1]
                value = value.lstrip()
                value = value.rstrip()
                if value == '':
                    raise Exception('At least, 1 line is not well formatted.')

                if "parse" in options:
                    self.path_dependencies = value
                elif "file" in options:
                    self.the_filenames = value.split(", ")
                elif "license" in options:
                    self.path_licenses = value

    def check(self, ins_file):

        if self.path_dependencies == str():
            raise Exception('The path containning the dependencies is not found in the ini file')
        if self.the_filenames == list():
            raise Exception('the filenames containning the dependencies are not found in the ini file')
        if self.path_licenses == str():
            raise Exception('The path to store the licenses is not found in the ini file')

        try:
            ins_file.check_the_directory(self.path_dependencies, True, False)
            ins_file.check_the_directory(self.path_licenses, True, False)
        except Exception as e:
            print('config.ini:', e.__str__())
            raise e()

    def get_the_config(self):

        ins_file = CFile()
        the_lines = ins_file.read_text_file (self.path, self.filename)
        self.extract_data_from_ini_file(the_lines)
        self.check(ins_file)
