#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.NetCDFInstaller import NetCDFInstaller
from tests.utils import BaseTestSetup


class TestNetCDFInstaller(unittest.TestCase):
    def setUp(self):
        """
        Set up global test parameters, and modify config.ini

        A back-up of config.ini is made prior to modification
        """

        self.base_setup = BaseTestSetup('netcdf')
        self.base_setup.set_up()

        # Setup the config path
        self.config = self.base_setup.test_config_ini_path

        self.installer = \
            NetCDFInstaller(config_path=self.config,
                            netcdf_log_path=None,
                            netcdf_cxx_log_path=None,
                            hdf5_log_path=None)

    def tearDown(self):
        """
        Remove created directories and files, restore config.ini
        """

        self.base_setup.tear_down()

    def test_netcdf(self):
        """
        Test that netcdf gets installed
        """

        self.installer.install()
        self.installer.install()
        self.assertTrue(self.installer.file_from_make.is_file())


if __name__ == '__main__':
    unittest.main()

