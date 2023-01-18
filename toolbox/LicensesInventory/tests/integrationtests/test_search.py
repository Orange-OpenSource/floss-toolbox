# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, MagicMock , patch
import os

from sources.common import CName, CFilter
from sources.configuration import CConfig
from sources.dependencies import CDependencies
from sources.search import CSearch, CDownload


class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_path = os.path.dirname(os.path.realpath(__file__))
        my_path_data = os.path.join(my_path, "data")
        cls.path_gradle = os.path.join(my_path_data, 'gradle')
        cls.path_package_json = os.path.join(my_path_data, 'package_json')
        
        ins_search = CSearch()
        cls.ins_search = ins_search

    @patch('sources.search.search.CFile.check_the_directory')
    @patch('sources.search.search.CDownload.get_file')
    def test_get_the_licenses_for_maven_central(self, mock_download_get_file, mock_file_check):
        ins_config = CConfig()
        ins_filter = CFilter()
        ins_dependencies = CDependencies()
        ins_search = CSearch()

        ins_config.path_source = self.path_gradle
        ins_config.the_filenames = ['dependency_maven_central.gradle']
        ins_config.path_curl = self.path_gradle
        ins_config.path_destination = self.path_gradle
        ins_config.path_dependencies = os.path.dirname(os.path.realpath(__file__))

        ins_filter.prepare(ins_config)
        the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)

        file_version = os.path.join(self.path_gradle, 'version_maven_central.json')
        file_license = os.path.join(self.path_gradle, 'license_maven_central.pom')
        mock_download_get_file.return_value = [file_license, file_version]
        the_licenses = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)

        self.assertEqual(1, len(the_licenses))
        from sources.common import CName
        ins_name = CName()
        license = the_licenses[ins_name.gradle]
        self.assertEqual(1, len(license))
        the_values = license[0]
        component = the_values[0]
        expected = 'mockito-core'
        self.assertEqual(expected, component)
        name = the_values[1]
        expected = 'mockito-core'
        self.assertEqual(expected, name)
        license_name = the_values[2]
        expected = 'The MIT License'
        self.assertEqual(expected, license_name)

    @patch('sources.search.search.CFile.check_the_directory')
    @patch('sources.search.search.CDownload.get_file')
    def test_get_the_licenses_for_github(self, mock_download_get_file, mock_file_check):
        ins_config = CConfig()
        ins_filter = CFilter()
        ins_dependencies = CDependencies()
        ins_search = CSearch()

        ins_config.path_source = self.path_gradle
        ins_config.the_filenames = ['dependency_github.gradle']
        ins_config.path_curl = self.path_gradle
        ins_config.path_destination = self.path_gradle        
        ins_config.path_dependencies = os.path.dirname(os.path.realpath(__file__))
        
        ins_filter.prepare(ins_config)
        the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)

        file_license = os.path.join(self.path_gradle, 'license_github.json')
        mock_download_get_file.return_value = [file_license, '']
        the_licenses = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)

        self.assertEqual(1, len(the_licenses))
        from sources.common import CName
        ins_name = CName()
        license = the_licenses[ins_name.gradle]
        self.assertEqual(1, len(license))
        the_values = license[0]
        component = the_values[0]
        expected = 'appcompat'
        self.assertEqual(expected, component)
        name = the_values[1]
        expected = 'AppCompat-Extension-Library'
        self.assertEqual(expected, name)
        license_name = the_values[2]
        expected = 'Apache License 2.0'
        
        self.assertEqual(expected, license_name)

    @patch('sources.search.search.CFile.check_the_directory')
    @patch('sources.search.search.CDownload.get_file')
    def test_get_the_licenses_for_package_json(self, mock_download_get_file, mock_file_check):
        ins_config = CConfig()
        ins_filter = CFilter()
        ins_dependencies = CDependencies()
        ins_search = CSearch()

        ins_config.path_source = self.path_package_json
        ins_config.the_filenames = ['package.json']
        ins_config.path_curl = self.path_package_json
        ins_config.path_destination = self.path_package_json
        ins_config.path_dependencies = os.path.dirname(os.path.realpath(__file__))

        ins_filter.prepare(ins_config)
        the_dependencies_by_platform = ins_dependencies.get_the_dependencies(ins_filter)

        file_license = os.path.join(self.path_package_json, 'license_package_json.html')
        mock_download_get_file.return_value = [file_license, '']
        the_licenses = ins_search.get_the_licenses(the_dependencies_by_platform, ins_config, ins_filter)

        self.assertEqual(1, len(the_licenses))
        from sources.common import CName
        ins_name = CName()
        license = the_licenses[ins_name.package_json]
        self.assertEqual(1, len(license))
        the_values = license[0]
        self.assertEqual(2, len(the_values))
        component = the_values[0]
        expected = '@popperjs/core'
        self.assertEqual(expected, component)
        license_name = the_values[1]
        expected = 'MIT'
        self.assertEqual(expected, license_name)
