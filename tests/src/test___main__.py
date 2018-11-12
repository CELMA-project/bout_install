#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import shutil
from pathlib import Path
from src.__main__ import main
from src.__main__ import add_str_to_bashrc
from tests.utils import BaseTestSetup


class TestMain(unittest.TestCase):
    def setUp(self):
        """
        Set up global test parameters, and modify config.ini

        A back-up of config.ini is made prior to modification
        """

        self.base_setup = BaseTestSetup('boutpp')
        self.base_setup.set_up()

        # Setup the config path
        self.config = self.base_setup.test_config_ini_path

    def tearDown(self):
        """
        Remove created directories and files, restore config.ini
        """

        self.base_setup.tear_down()

    def test_main(self):
        """
        Test that the main function is working
        """

        # FIXME: You are here
        # FIXME: Refactor
        # FIXME: Make a setup.py and add to pip
        # main(self.config)
        # NOTE: Here we test main
        # After build one of the bout-stuff to see that it is working

        pass


class TestMainHelpers(unittest.TestCase):
    def setUp(self):
        """
        Make a backup of .bashrc (makes the file if it doesn't exist)
        """

        self.bashrc_path = Path.home().joinpath('.bashrc')
        self.exist = self.bashrc_path.is_file()
        if not self.exist:
            self.bashrc_path.touch()

        self.bashrc_bak_path = Path.home().joinpath('.bashrc.bak')
        shutil.copy(self.bashrc_path, self.bashrc_bak_path)

    def tearDown(self):
        """
        Move .bashrc.bak to .bashrc
        """

        shutil.copy(self.bashrc_bak_path, self.bashrc_path)
        self.bashrc_bak_path.unlink()

        if not self.exist:
            self.bashrc_path.unlink()

    def test_add_str_to_bashrc(self):
        """
        Test that we can add to bashrc
        """

        expected = '# harmless string'
        add_str_to_bashrc(expected)

        with self.bashrc_path.open('r') as f:
            lines = f.readlines()

        self.assertEqual(expected, lines[-1])


if __name__ == '__main__':
    unittest.main()

