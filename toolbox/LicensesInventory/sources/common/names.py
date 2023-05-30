#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Laurent BODY <laurent(dot)body(at)orange(dot)com> et al.

class CName:

    def __init__(self):
        self.component = 'component'
        self.namespace = 'namespace'
        self.version = 'version'
        self.gradle = 'gradle'
        self.github = 'github'
        self.version_for_maven_central = 'version'
        self.maven_central = 'maven_central'
        self.package_json = 'package.json'
        self.roast = 'Cargo.lock'
        self.go = 'go.mod'
        self.go_github = 'go github'
        self.flutter = 'pubspec.yaml'
        self.swift = 'Package.swift'
        self.cocoapods = 'Podfile'
        self.elm_lang = 'elm.json' #unable: no result in the response of the request

    def get_the_platforms(self):
        r = [self.gradle]
        r += [self.package_json]
        r += [self.roast]
        r += [self.go]
        r += [self.flutter]
        r += [self.swift]
        r += [self.cocoapods]
        r += [self.elm_lang]
        return r
