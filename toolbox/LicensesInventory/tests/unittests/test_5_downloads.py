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

import unittest
from unittest.mock import patch, MagicMock
import requests
import os

from sources.common import CName, CFilter
from sources.search import CDownload


class TestDownloads(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")

        path_licenses = os.path.join(path_data, "licenses_for_downloads")
        cls.path_licenses = path_licenses

        path_sources = os.path.join(path_licenses, "sources")
        cls.path_sources = path_sources

        path_results = os.path.join(path_licenses, "results")
        cls.path_results = path_results

        cls.ins_name = CName()
        cls.ins_download = CDownload()

    @patch('sources.search.downloads.requests.get')
    def atest_1_requests_get_OK(self, mock_requests_get):
        # requests
        response = requests.models.Response
        response.status_code = '200'
        response.text = 'line_a\nline_b'
        mock_requests_get.return_value = response

        # inputs
        platform = CName().github

        the_key_and_dependency = dict()
        component = 'gradle.c/a'
        the_key_and_dependency[CName().component] = component

        namespace = 'gradle_n_a'

        ins_download = CDownload()

        ins_filter = CFilter()

        ins_filter.the_URLs = dict()
        ins_filter.the_URLs[platform] = "https://api.github.com/search/repositories?q=[component]"

        filename = component + '_' + namespace
        expected_filename = filename.replace('.', '_')
        expected_filename = expected_filename.replace('/', '_')
        expected_filename += '_github.json'
        ins_filter.the_filenames[platform] = expected_filename

        ins_download.ins_filter = ins_filter

        expected_file = os.path.join(self.path_licenses, expected_filename)
        ins_download.write_in_file = MagicMock()
        ins_download.write_in_file.return_value = expected_file
        ins_download.manage_sleep = MagicMock()

        file = ins_download.get_file(platform, the_key_and_dependency, namespace)

        #fichier vide : ok
        #fichier avec lignes contenant des espaces : 

        self.assertEqual(expected_file, file)
        ins_download.manage_sleep.assert_called_once()
        ins_download.write_in_file.assert_called_once()

    @patch('sources.search.downloads.requests.get')
    def atest_2_requests_get_KO(self, mock_requests_get):
        # requests
        response = requests.models.Response
        response.status_code = '300'
        response.text = 'line_a\nline_b'
        mock_requests_get.return_value = response

        # inputs
        platform = CName().github

        the_key_and_dependency = dict()
        component = 'gradle.c/a'
        the_key_and_dependency[CName().component] = component

        namespace = 'gradle_n_a'

        ins_download = CDownload()

        ins_filter = CFilter()

        ins_filter.the_URLs = dict()
        ins_filter.the_URLs[platform] = "https://api.github.com/search/repositories?q=[component]"

        filename = component + '_' + namespace
        expected_filename = filename.replace('.', '_')
        expected_filename = expected_filename.replace('/', '_')
        expected_filename += '_github.json'
        ins_filter.the_filenames[platform] = expected_filename

        ins_download.ins_filter = ins_filter

        expected_file = os.path.join(self.path_licenses, expected_filename)
        ins_download.write_in_file = MagicMock()
        #ins_download.write_in_file.return_value = expected_file
        ins_download.manage_sleep = MagicMock()

        file = ins_download.get_file(platform, the_key_and_dependency, namespace)

        self.assertEqual(None, file)
        self.assertEqual(None, ins_download.manage_sleep.assert_called())

    @patch('sources.search.downloads.requests.get')
    def test_3_retry_after(self, mock_requests_get):
        # requests
        response = requests.models.Response
        response.status_code = '300'
        #response.retry_after = '184'
        response.retry_after = 'Mon, 22 Feb 2024 17:00:00 GMT'
        # mocker la date courrante : datetime.now
        response.text = 'line_a\nline_b'
        mock_requests_get.return_value = response

        # inputs
        platform = CName().github

        the_key_and_dependency = dict()
        component = 'gradle.c/a'
        the_key_and_dependency[CName().component] = component

        namespace = 'gradle_n_a'

        ins_download = CDownload()

        ins_filter = CFilter()

        ins_filter.the_URLs = dict()
        ins_filter.the_URLs[platform] = "https://api.github.com/search/repositories?q=[component]"

        filename = component + '_' + namespace
        expected_filename = filename.replace('.', '_')
        expected_filename = expected_filename.replace('/', '_')
        expected_filename += '_github.json'
        ins_filter.the_filenames[platform] = expected_filename

        ins_download.ins_filter = ins_filter

        expected_file = os.path.join(self.path_licenses, expected_filename)
        ins_download.write_in_file = MagicMock()
        ins_download.manage_sleep = MagicMock()

        file = ins_download.get_file(platform, the_key_and_dependency, namespace)

        self.assertEqual(None, file)
        self.assertEqual(None, ins_download.manage_sleep.assert_called())
        self.assertNotEqual(None, ins_download.next_date)
        self.assertNotEqual(None, ins_download.delay)
