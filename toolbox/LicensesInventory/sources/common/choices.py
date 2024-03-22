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


class CChoice:

    def __init__(self):
        self.all = 'all'
        self.only_the_dependencies_on_error = 'only_the_dependencies_on_error'
        self.only_the_new_dependencies = 'only_the_new_dependencies'
        self.quit = 'quit'
