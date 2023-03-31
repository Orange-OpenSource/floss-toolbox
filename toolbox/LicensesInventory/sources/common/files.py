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


class CFile:

    def delete_the_files_in_path(self, path):
        name = 'delete_the_files_in_path'

        if os.path.isdir(path) == False:
            raise Exception('\t💥  ' + name + ': The path does not exist.\n' + path)

        for root, dirs, files in os.walk(path):
            for file in files:
                filename = os.path.join(path, file)
                os.remove(filename)

    def get_the_files_by_names(self, path, filename):
        name = 'get_the_files_by_names'
        the_files = list()

        if os.path.isdir(path) == False:
            raise Exception('\t💥  ' + name + ': the path to parse the files which contain the dependencies does not exist.')
        if filename == '' or filename == None:
            raise Exception('\t💥  ' + name + ': the filename is not precised.')

        for root, dirs, files in os.walk(path):
            for file in files:
                if file == filename:
                    the_files.append(os.path.join(root, filename))

        if len(the_files) < 1:
            raise Exception('\t💥  ' + name + ': no file to parse.')

        return the_files

    def ask_before_creating_directory(self, my_path):
        response = ""

        line_1 = 'Do you want to create the directory ?'
        line_2 = '  \'' + my_path + '\''
        line_3 = '  yes: \'y\' or \'Y\', no: \'n\' or \'N\' > '
        while response == '':
            response = input(line_1 + '\n' + line_2 + '\n' + line_3)
        the_responses_to_create = ['y', 'Y']
        if response in the_responses_to_create:
            return True

        return False

    def check_the_directory(self, my_path, to_create, to_ask):

        if os.path.isdir(my_path) == True:
            return True

        if to_create == False:
            return False
        if to_ask == True:
            if self.ask_before_creating_directory(my_path) == False:
                return False

        try:
            os.makedirs(my_path)
        except Exception as e:
            raise e

        return True

    def write_in_text_file(self, path='', filename='', the_lines=list()):
        name = 'write_in_text_file'

        if self.check_the_directory(path, False, False) == False:
            raise Exception('\t💥  ' + name + ': the directory does not exist.\n' + path)

        if filename == '':
            filename = path
        else:
            filename = os.path.join(path, filename)

        if the_lines == None or len(the_lines) == 0:
            raise Exception('\t💥  ' + name + ': no data to write.')

        try:
            with open(filename, 'wt', encoding='utf-8') as f:
                for line in the_lines:
                    line = line + '\n'
                    f.write(line)
        except:
            raise Exception('\t💥  ' + ame + ': the path exists, but, impossible to write in.')

    def read_text_file (self, path, filename=''):
        the_lines = list()

        if self.check_the_directory(path, False, False) == False:
            raise Exception('\t💥  ' + name + ': the directory does not exist.\n' + path)

        if filename == '':
            filename = path
        else:
            filename = os.path.join(path, filename)

        if os.path.isfile(filename) == False:
            raise Exception('\t💥  ' + name + ': no file to read.')

        try:
            with open(filename, 'rt', encoding='utf-8') as f:
                the_lines = f.read().split('\n')
        except:
            raise Exception('\t💥  ' + name + ': the file exists, but, impossible to read.\n', filename)

        return the_lines

    def manage(self, the_licenses, my_path):

        for k, v in the_licenses.items():
            key = k.replace('.', '_')
            filename = 'licenses_' + key + '.txt'
            filename = os.path.join(my_path, filename)

            with open(filename, 'wt', encoding='utf-8') as f:
                for a, b, c in v:
                    if b == None:
                        b = 'None'
                        c = 'None'
                    f.write(a + ' : ' + b + ' : ' + c + '\n')

    def get_the_files(self, path, the_names):
        result = list()

        the_files = list()
        for name in the_names:
            the_files += self.get_the_files_by_names(path, name)

        for file in the_files:
            file = file.lower()
            result.append(file)

        return result

