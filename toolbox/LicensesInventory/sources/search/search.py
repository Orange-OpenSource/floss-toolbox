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

from sources.common import CName, CFile
from .downloads import CDownload
from .parsings import CParsing


class CSearch:
    """
    Get the licenses: for each platform and for each component
    """

    def __init__(self):
        self.ins_name = CName()
        self.ins_download = CDownload()
        self.ins_parsing = CParsing()
        #self.ins_filter = None
        #self.ins_config = None
        self.ins_file = CFile()
        self.the_dependencies_on_error_by_platform = None

    def get_license_for_others(self, platform, dependency):
        the_values_for_license = list()

        component = dependency[0]
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        file = self.ins_download.get_file(platform, the_key_and_dependency, None)
        if file == None: return the_values_for_license

        if platform == self.ins_name.roast:
            the_values_for_license = self.ins_parsing.get_license_for_roast(file)
        else:
            the_values_for_license = self.ins_parsing.get_license_with_html(file)

        return the_values_for_license

    def get_license_for_gradle(self, platform, dependency):
        the_values_for_license = list()

        component = dependency[0]
        namespace = None
        if len(dependency) > 1:
            namespace = dependency[1]

        platform = self.ins_name.github
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        file = self.ins_download.get_file(platform, the_key_and_dependency, namespace)
        if file != None:
            the_values_for_license = self.ins_parsing.get_license_for_github(file)
            return the_values_for_license

    def maven_central_does_not_work():
        # maven central
        version = None
        namespace = dependency[1]
        if (namespace != str()) and (namespace != None):
            platform = self.ins_name.version_for_maven_central
            the_key_and_dependency[self.ins_name.namespace] = namespace
            file = self.ins_download.get_file(platform, the_key_and_dependency, None)
            if file == None:
                return bad_result
            version= self.ins_parsing.extract_version_for_maven_central(file)
            os.remove(file)
            if version == None:
                return bad_result

            platform = self.ins_name.maven_central
            the_key_and_dependency = dict()
            new_component = component.replace('.', '/')
            the_key_and_dependency[self.ins_name.component] = new_component
            new_namespace = namespace.replace('.', '/')
            the_key_and_dependency[self.ins_name.namespace] = new_namespace
            the_key_and_dependency[self.ins_name.version] = version
            file = self.ins_download.get_file(platform, the_key_and_dependency, None)
            if file == None:
                return bad_result
            license_central = self.ins_parsing.get_license_for_maven_central(file)
            if license_central == None:
                return bad_result
            return license_central

    def get_license_for_go(self, platform, dependency):
        the_values_for_license = list()

        component = dependency[0]

        if 'github' in component:
            platform = self.ins_name.go_github
        else:
            platform = self.ins_name.go

        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        file = self.ins_download.get_file(platform, the_key_and_dependency, None)
        if file == None:
            return the_values_for_license

        the_values_for_license = self.ins_parsing.get_license_with_html(file)

        return the_values_for_license

    def extract_the_licenses(self, platform, the_dependencies, number_of_errors_max):
        the_licenses = list()
        the_errors = list()

        to_treat = True
        number_of_errors = 0
        for i_dependency in range(0, len(the_dependencies)):
            dependency = the_dependencies[i_dependency]
            component = dependency[0]

            if number_of_errors == number_of_errors_max:
                to_treat = False

            the_values_for_license = list()
            if to_treat == True:
                print(platform, ':', component)
                if platform == self.ins_name.gradle:
                    the_values_for_license = self.get_license_for_gradle(platform, dependency)
                elif platform == self.ins_name.go:
                    the_values_for_license = self.get_license_for_go(platform, dependency)
                elif platform != None:
                    the_values_for_license = self.get_license_for_others(platform, dependency)

            error_code = int(self.ins_download.error_code)
            if error_code < 300:
                number_of_errors = 0
                the_licenses.append(dependency + the_values_for_license)
            else:
                field_error_code = ['error code = ' + self.ins_download.error_code]
                if to_treat == False:
                    dependency += ['successive authorized errors at ' + str(number_of_errors)]
                else:
                    number_of_errors += 1
                the_errors.append(field_error_code + dependency)

        if to_treat == False:
            if self.ins_download.next_date != None:
                text = 'retry after ' + self.ins_download.next_date
                text += ' - in ' + self.ins_download.delay
                the_errors.insert(0, [text])

        return (the_licenses, the_errors)

    def get_the_platforms(self, a, b):
        the_platforms = list(a.keys())
        the_platforms += list(b.keys())

        # delete the duplicated platforms
        d = dict()
        for p in the_platforms:
            d[p] = str()
        the_platforms = list(d.keys())

        return the_platforms

    def get_the_licenses(self, the_dependencies_by_platform, ins_config, ins_filter):
        result = dict()
        result_on_error = dict()

        self.ins_download.ins_filter = ins_filter

        for platform, the_dependencies in the_dependencies_by_platform.items():
            sub_folder = platform.replace('.', '_')
            self.ins_download.path_licenses = os.path.join(ins_config.path_licenses, sub_folder)

            r =self.extract_the_licenses(platform, the_dependencies, ins_config.number_of_errors_max)
            the_licenses, the_errors = r
            if len(the_licenses) > 0:
                result[platform] = the_licenses
            if len(the_errors) > 0:
                result_on_error[platform] = the_errors

        return (result, result_on_error)
