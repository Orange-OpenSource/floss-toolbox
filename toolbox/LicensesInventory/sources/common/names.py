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


class CName:

    def __init__(self):
        self.component = 'component'
        self.namespace = 'namespace'
        self.version = 'version'

        self.gradle = 'gradle'
        self.package_json = 'package.json'
        self.roast = 'Cargo.lock'
        self.go = 'go.mod'
        self.flutter = 'pubspec.yaml'
        self.swift = 'Package.swift'
        self.cocoapods = 'Podfile'
        #self.elm_lang = 'elm.json' #unable: no result in the response of the request

        self.github = 'github'
        self.go_github = 'go github'

        self.separator_between_fields_in_file = ' : '

        self.version_for_maven_central = 'version'
        self.maven_central = 'maven_central'

    def get_the_platforms(self):
        r = [self.gradle]
        r += [self.package_json]
        r += [self.roast]
        r += [self.go]
        r += [self.flutter]
        r += [self.swift]
        r += [self.cocoapods]
        return r
