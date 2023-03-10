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

from sources.common import CName, CFile
from .downloads import CDownload
from .parsings import CParsing

class CSearch:
    """
    Helps to get the licenses for each platform and for each dependency.
    """

    def __init__(self):
        self.ins_name = CName()
        self.ins_download = CDownload()
        self.ins_parsing = CParsing()
        self.msg_download_license = 'downloading the license'
        self.msg_parse_license = 'parsing the file containning the license'
        self.msg_download_version = 'downloading the version'
        self.msg_parse_version = 'parsing the file containning the version'
        self.the_licenses = list()

    def get_the_licenses_for_others(self, platform, dependency):
        """
        Request online platforms and forges and scraps them to extract meaningful details.
        Then parses the extracted file.
        Only JavaScript/Node.js (package.json), Rust (Cargo.lock), Go (go.mod), Flutter (pubspec.yaml)
        and Swift (Package.swift) are managed.
        """

        print('\t➡️  Getting the licenses for others...')
        bad_result = [None]

        component = dependency[0]
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        the_files = self.ins_download.get_file(platform, the_key_and_dependency, [''], 0)
        if the_files == None:
            return bad_result

        file = the_files[0]
        result = list()
        if platform == self.ins_name.package_json:
            result = self.ins_parsing.get_license_for_package_json(file)
        elif platform == self.ins_name.roast:
            result = self.ins_parsing.get_license_for_roast(file)
        elif platform == self.ins_name.flutter:
            result = self.ins_parsing.get_license_for_flutter(file)
        elif platform == self.ins_name.swift:
            result = self.ins_parsing.get_license_for_swift(file)

        if result == None:
            return bad_result

        print('\t\t✅ Getting the licenses for others... OK!')
        return result

    def get_the_licenses_for_gradle(self, platform, dependency):
        """
        Requests GitHub or Maven Central to get licences of Gradle file
        """

        print('\t➡️  Getting the licenses for Gradle...')
        bad_result = [None]

        component = dependency[0]

        platform = self.ins_name.github
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        the_files = self.ins_download.get_file(platform, the_key_and_dependency, ['', ''], 0)
        if the_files != None:
            file = the_files[0]
            license_github = self.ins_parsing.get_license_for_github(file)
            if license_github != None:
                return license_github

        # maven central
        version = None
        namespace = dependency[1]
        if (namespace != str()) and (namespace != None):
            platform = self.ins_name.version_for_maven_central
            the_key_and_dependency[self.ins_name.namespace] = namespace
            the_files = self.ins_download.get_file(platform, the_key_and_dependency, ['', ''], 1)
            if the_files == None:
                return bad_result
            file = the_files[1]
            version= self.ins_parsing.extract_version_for_maven_central(file)
            if version == None:
                return bad_result

            platform = self.ins_name.maven_central
            the_key_and_dependency = dict()
            new_component = component.replace('.', '/')
            the_key_and_dependency[self.ins_name.component] = new_component
            new_namespace = namespace.replace('.', '/')
            the_key_and_dependency[self.ins_name.namespace] = new_namespace
            the_key_and_dependency[self.ins_name.version] = version
            the_files = self.ins_download.get_file(platform, the_key_and_dependency, ['', ''], 0)
            if the_files == None:
                return bad_result
            file = the_files[0]
            license_central = self.ins_parsing.get_license_for_maven_central(file)
            if license_central == None:
                return bad_result
            return license_central

        print('\t\t✅ Getting the licenses for Gradle... OK!')
        return bad_result

    def get_the_licenses_for_go(self, platform, dependency):
        """
        Requests GitHub or other platform to get licences of go.mod file
        """

        print('\t➡️  Getting the licenses for Go...')
        bad_result = [None]

        component = dependency[0]

        if 'github' in component:
            platform = self.ins_name.go_github
        else:
            platform = self.ins_name.go

        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.component] = component
        the_files = self.ins_download.get_file(platform, the_key_and_dependency, ['', ''], 0)
        if the_files != None:
            file = the_files[0]
            license = [str()]
            if platform == self.ins_name.go_github:
                license = self.ins_parsing.get_license_for_go_github(file)
            elif platform == self.ins_name.go:
                license = self.ins_parsing.get_license_for_go(file)
            if license != None:
                return license

        print('\t\t✅ Getting the licenses for Go... OK!')
        return bad_result

    def get_the_licenses(self, the_dependencies_by_platform, ins_config, ins_filter):
        """
        Get licences for Gradle files or Go files or other types of files.
        """
        
        print('\t➡️  Getting the licenses for some...')
        result = dict()

        self.ins_filter = ins_filter
        self.ins_download.ins_filter = ins_filter
        self.ins_download.path_licenses = ins_config.path_licenses
        ins_file = CFile()

        for platform, the_dependencies in the_dependencies_by_platform.items():
            the_licenses = list()
            sub_folder = platform.replace('.', '_')
            self.ins_download.path_licenses = os.path.join(self.ins_download.path_licenses, sub_folder)
            ins_file.check_the_directory(self.ins_download.path_licenses, True, False)
            for dependency in the_dependencies:
                # add component
                license = [dependency[0]]
                # print("\t🔨  Dependency / platform = ", dependency[0], ':', platform)
                if platform == self.ins_name.gradle:
                    license += self.get_the_licenses_for_gradle(platform, dependency)
                elif platform == self.ins_name.go:
                    license += self.get_the_licenses_for_go(platform, dependency)
                else:
                    license += self.get_the_licenses_for_others(platform, dependency)
                the_licenses.append(license)
            result[platform] = the_licenses

        print('\t\t✅ Getting the licenses for some... OK!')
        return result
