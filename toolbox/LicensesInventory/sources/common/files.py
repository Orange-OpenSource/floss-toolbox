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

from sources.common import CDate

class CErrorCode():
    def __init__(self):
        self.isdir = 'The path is not correct !'
        self.exists = 'The path does not exist !'
        self.isfile = 'The filename does not exist !'

class CFileException(Exception):
    def __init__(self, msg, filename):
        super().__init__(msg + '\n\tfilename ' + filename)

class CFile:

    def __init__(self):
        self.separator = ' : '
        self.last_field_for_duplicated = 'DUPLICATED'
        self.space = ' '
        self.ins_date = CDate()

    def delete_the_files_in_path(self, path):
        for root, dirs, files in os.walk(path):
            for filename in files:
                file = os.path.join(path, filename)
                os.remove(file)

    def get_the_files_by_names(self, path, filename):
        the_files = list()

        for root, dirs, files in os.walk(path):
            for file in files:
                if file == filename:
                    the_files.append(os.path.join(root, filename))

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

    def get_file_from_path_and_filename(self, path, filename):

        file = path
        if filename != str():
            file = os.path.join(path, filename)

        return file

    def write_in_text_file(self, path=str(), filename=str(), the_lines=list()):
        file = self.get_file_from_path_and_filename(path, filename)
        with open(file, 'wt', encoding='utf-8') as f:
            for line in the_lines:
                line = line + '\n'
                f.write(line)

    def read_text_file (self, path, filename=''):
        the_lines = list()

        file = os.path.join(path, filename)
        with open(file, 'rt', encoding='utf-8') as f:
            the_lines = f.read().split('\n')

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
                    f.write(a + self.separator + b + self.separator + c + '\n')

    def get_the_files(self, path, the_names):
        result = list()

        the_files = list()
        for name in the_names:
            the_files += self.get_the_files_by_names(path, name)

        for file in the_files:
            file = file.lower()
            result.append(file)

        return result

    def get_the_lines_from_the_new_licenses(self, the_licenses):
        result = list()

        for license in the_licenses:
            line = str()
            for field in license:
                if field == None or field == str():
                    field = 'None'
                if line == str():
                    line = field
                else:
                    line += self.separator + field
            result.append(line)

        return result

    def extract_the_lines_to_write(self, the_old_lines, the_new_lines, comment, my_date):
        result = list()

        if len(the_old_lines) == 0:
            result = [comment]
        else:
            result = the_old_lines[:]

        result += [my_date]
        result += the_new_lines

        return result

    def rename_original_filename(original_filename):
        p_extension = original_filename.find('.')
        extension = original_filename[p_extension:]
        filename = original_filename[:p_extension]

        current_date = self.ins_date.get_date_and_time().replace(':', '_')
        current_date = current_date.replace(':', '_')

        return filename + '_' + current_date + extension

    def save_the_licenses(self, the_licenses_by_platform, ins_config):
        result = list()

        comment = '# If the license is at None, or not clear, you are invited to search in the downloaded file.'
        path = ins_config.path_licenses
        my_date = CDate().prefix_for_date + CDate().get_date_and_time()
        for platform, the_licenses in the_licenses_by_platform.items():
            filename = ins_config.filename_for_the_licenses.replace('[platform]', platform)
            file = os.path.join(path, filename)
            old_filename = filename.replace('.txt', '.old')
            old_file = os.path.join(path, old_filename)

            the_old_lines = self.manage_old_lines(path, filename)
            the_new_lines = self.get_the_lines_from_the_new_licenses(the_licenses)
            the_lines = self.extract_the_lines_to_write(the_old_lines, the_new_lines, comment, my_date)

            if len(the_old_lines) > 0:
                os.rename(file, old_file)

            self.write_in_text_file(path, filename, the_lines)
            result += the_lines

            if len(the_old_lines) > 0:
                os.remove(old_file)

        return result

    def save_the_errors(self, the_new_dependencies_on_error_by_platform, ins_config):
        result = list()

        path = ins_config.path_errors
        my_date = CDate().prefix_for_date + CDate().get_date_and_time()
        for platform, the_new_dependencies_on_error in the_new_dependencies_on_error_by_platform.items():
            filename = ins_config.model_for_errors_file.replace('[platform]', platform)
            file = os.path.join(path, filename)
            old_filename = filename.replace('.txt', '.old')
            old_file = os.path.join(path, old_filename)

            the_old_lines = self.manage_old_lines(path, filename)
            the_new_lines = self.manage_new_lines(the_new_dependencies_on_error)

            if len(the_old_lines) > 0:
                os.rename(file, old_file)

            the_lines = the_old_lines + [my_date] + the_new_lines
            self.write_in_text_file(path, filename, the_lines)
            result += the_lines

            if len(the_old_lines) > 0:
                os.remove(old_file)

        return result

    def manage_new_lines(self, the_new_dependencies_on_error):
        the_new_lines = list()
        for new_dependency_on_error in the_new_dependencies_on_error:
            line = str()
            for value in new_dependency_on_error:
                if value == None or value == str():
                    value = 'None'
                if line == str():
                    line+= value
                else:
                    line += self.separator + value
            the_new_lines += [line]

        return the_new_lines

    def manage_old_lines(self, path, filename):
        the_old_lines = list()
        try:
            the_old_lines = self.read_text_file (path, filename)
        except Exception as e:
            the_old_lines = list()

        the_tmp = the_old_lines[:]
        the_old_lines = list()
        for tmp in the_tmp:
            line = tmp.strip()
            if line != str():
                the_old_lines.append(line)

        return the_old_lines

    def delete_file(self, path, filename):

        file = os.path.join(path, filename)
        if os.path.isfile(file) == True:
            os.remove(file)
