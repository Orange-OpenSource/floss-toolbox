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

    def get_the_licenses_for_others(self, platform, dependency):
        print('\t➡️  Getting the licenses for others...')
        bad_result = [None]

        component = dependency[0]
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        file = self.ins_download.get_file(platform, the_key_and_dependency)
        if file == None: return bad_result

        result = bad_result
        if platform == self.ins_name.roast:
            result = self.ins_parsing.get_license_for_roast(file)
        else:
            result = self.ins_parsing.get_license_with_html(file)

        if result == None:
            result = bad_result

        print('\t\t✅ Getting the licenses for others... OK!')            
        return result

    def get_the_licenses_for_gradle(self, platform, dependency):
        print('\t➡️  Getting the licenses for Gradle...')
        bad_result = [None]

        component = dependency[0]

        platform = self.ins_name.github
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        file = self.ins_download.get_file(platform, the_key_and_dependency)
        if file != None:
            license_github = self.ins_parsing.get_license_for_github(file)
            if license_github != None:
                return license_github

        return bad_result

    def maven_central_does_not_work():
        # maven central
        version = None
        namespace = dependency[1]
        if (namespace != str()) and (namespace != None):
            platform = self.ins_name.version_for_maven_central
            the_key_and_dependency[self.ins_name.namespace] = namespace
            file = self.ins_download.get_file(platform, the_key_and_dependency)
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
            file = self.ins_download.get_file(platform, the_key_and_dependency)
            if file == None:
                return bad_result
            license_central = self.ins_parsing.get_license_for_maven_central(file)
            if license_central == None:
                return bad_result
            return license_central

    def get_the_licenses_for_go(self, platform, dependency):
        print('\t➡️  Getting the licenses for Go...')
        bad_result = [None]

        component = dependency[0]

        if 'github' in component:
            platform = self.ins_name.go_github
        else:
            platform = self.ins_name.go

        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        file = self.ins_download.get_file(platform, the_key_and_dependency)
        if file != None:
            license = [str()]
            if platform == self.ins_name.go_github:
                license = self.ins_parsing.get_license_for_go_github(file)
            elif platform == self.ins_name.go:
                license = self.ins_parsing.get_license_for_go(file)
            if license != None:
                return license

        return bad_result

    def get_the_licenses(self, the_dependencies_by_platform, ins_config, ins_filter):
        print('\t➡️  Getting the licenses for some...')
        result = dict()
        on_error = dict()

        self.ins_filter = ins_filter
        self.ins_download.ins_filter = ins_filter
        ins_file = CFile()

        for platform, the_dependencies in the_dependencies_by_platform.items():
            the_licenses = list()
            sub_folder = platform.replace('.', '_')
            self.ins_download.path_licenses = os.path.join(ins_config.path_licenses, sub_folder)
            ins_file.check_the_directory(self.ins_download.path_licenses, True, False)
            for i_dependency in range(0, len(the_dependencies)):
                dependency = the_dependencies[i_dependency]
                license = dependency[:]
                print(dependency[0], ':', platform)
                r = None
                if platform == self.ins_name.gradle:
                    r = self.get_the_licenses_for_gradle(platform, dependency)
                elif platform == self.ins_name.go:
                    r = self.get_the_licenses_for_go(platform, dependency)
                else:
                    r = self.get_the_licenses_for_others(platform, dependency)
                error_code = int(self.ins_download.error_code)
                if error_code == 403:
                    on_error[platform] = the_dependencies[i_dependency:]
                    break # the_dependencies
                if error_code > 299:
                    r = ['error code=' + str(error_code)]
                    r = ['error code=' + str(error_code)]
                license += r
                the_licenses.append(license)
            result[platform] = the_licenses

        return (result, on_error)
