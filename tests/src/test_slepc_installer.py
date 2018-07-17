#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.SLEPcInstaller import SLEPcInstaller
from tests.utils import BaseTestSetup


class TestSLEPcInstaller(unittest.TestCase):
    def setUp(self):
        """
        Set up global test parameters, and modify config.ini

        A back-up of config.ini is made prior to modification
        """

        self.base_setup = BaseTestSetup('slepc')
        self.base_setup.set_up()

        # Setup the config path
        self.config = self.base_setup.test_config_ini_path

        self.installer = SLEPcInstaller(config_path=self.config, mpi_log_path=None)

    def tearDown(self):
        """
        Remove created directories and files, restore config.ini
        """

        self.base_setup.tear_down()

    def test_slepc(self):
        """
        Test that slepc gets installed
        """

        self.installer.install()
        self.installer.install()
        self.assertTrue(self.installer.file_from_make.is_file())


if __name__ == '__main__':
    unittest.main()

