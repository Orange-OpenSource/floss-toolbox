#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import requests
import os

from sources.common import CName, CFilter
from sources.search import CDownload


class TestDownloads(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        path_data = os.path.join(my_path, "data")

        path_licenses = os.path.join(path_data, "licenses_for_tests")
        cls.path_licenses = path_licenses

        path_sources = os.path.join(path_licenses, "sources")
        cls.path_sources = path_sources

        path_results = os.path.join(path_licenses, "results")
        cls.path_results = path_results

        cls.ins_name = CName()
        cls.ins_download = CDownload()

    @patch('sources.search.downloads.CFile.write_in_text_file')
    def test_1_write_in_file(self, mock_CFile_write_in_text_file):

        # inputs
        self.ins_download.path_licenses = self.path_licenses
        filename = 'component.mytest'

        # mock and expected
        expected_file = os.path.join(self.ins_download.path_licenses, filename)
        mock_CFile_write_in_text_file.return_value = expected_file

        # inputs for the method
        status_code = '299'
        text = 'line_a\nline_b'
        response = requests.models.Response
        response.status_code = status_code
        response.text = text

        file = self.ins_download.write_in_file(response, filename)

        content = response.text
        the_lines = content.split('\n')
        self.ins_download.ins_file.write_in_text_file.assert_called_once_with(self.ins_download.path_licenses, filename, the_lines)

        self.assertEqual(expected_file, file)

    @patch('sources.search.downloads.CFile.write_in_text_file')
    @patch('sources.search.downloads.requests.get')
    def test_2_get_file(self, mock_requests_get, mock_CFile_write_in_text_file):
        # source: build.gradle

        # inputs for the method
        platform = self.ins_name.github
        # appcompat : appcompatprocessor : Apache License 2.0
        the_key_and_dependency = dict()
        the_key_and_dependency[self.ins_name.namespace] = 'my_namespace'
        the_key_and_dependency[self.ins_name.component] = 'appcompat'

        # before executing ins_download.get_file
        ins_filter = CFilter()
        the_urls = dict()
        the_urls[self.ins_name.github] = "my_url"
        ins_filter.the_URLs = the_urls
        the_filenames = dict()
        the_filenames[self.ins_name.github] = '[component]_github.json'
        ins_filter.the_filenames = the_filenames
        self.ins_download.ins_filter = ins_filter

        self.ins_download.path_licenses = os.path.join(self.path_licenses, self.ins_name.gradle)
        filename = 'appcompat_github.json'
        expected_file = os.path.join(self.ins_download.path_licenses, filename)
        mock_CFile_write_in_text_file.return_value = expected_file

        expected_response = requests.models.Response
        expected_response.status_code = '299'
        expected_response.text = 'line_a\nline_b'
        mock_requests_get.return_value = expected_response

        file = self.ins_download.get_file(platform, the_key_and_dependency)
        self.assertEqual(expected_file, file)
