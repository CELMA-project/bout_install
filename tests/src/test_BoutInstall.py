#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import shutil
from pathlib import Path
from src.BoutInstall import BoutInstall


class TestBoutInstall(unittest.TestCase):
    def setUp(self):
        """
        Set up global test parameters
        """

        self.installer = BoutInstall()
        root_dir = Path(__file__).absolute().parents[2]
        self.main_dir = root_dir.joinpath('test_main_dir')
        self.other_dir = root_dir.joinpath('test_other_dir')

    def tearDown(self):
        """
        Remove created directories and files
        """

        shutil.rmtree(self.main_dir, ignore_errors=True)
        shutil.rmtree(self.other_dir, ignore_errors=True)

    def test__setup_logger(self):
        """
        Test that the logger is working
        """

        log_path = self.main_dir.joinpath('test.log')
        installer = BoutInstall(log_path)
        installer.logger.info('This is a test')
        self.assertTrue(log_path.is_file())

    def test_set_install_dirs(self):
        """
        Tests that the directories are properly installed
        """

        self.installer.set_install_dirs(main_dir=self.main_dir)
        install_dir = self.main_dir.joinpath('install')
        local_dir = self.main_dir.joinpath('local')
        examples_dir = self.main_dir.joinpath('examples')
        self.assertTrue(install_dir.is_dir())
        self.assertTrue(local_dir.is_dir())
        self.assertTrue(examples_dir.is_dir())

        install_dir = self.other_dir.joinpath('install')
        local_dir = self.other_dir.joinpath('local')
        examples_dir = self.other_dir.joinpath('examples')
        self.installer.set_install_dirs(install_dir=install_dir,
                                        local_dir=local_dir,
                                        examples_dir=examples_dir)
        self.assertTrue(install_dir.is_dir())
        self.assertTrue(local_dir.is_dir())
        self.assertTrue(examples_dir.is_dir())

    def test_get_tar_file(self):
        """
        Tests that the .tar files can be downloaded
        """

        self.assertRaises(RuntimeError,
                          self.installer.get_tar_file,
                          url=self.installer.fftw_url)
        self.installer.set_install_dirs(main_dir=self.main_dir)
        tar_file_path = \
            self.installer.get_tar_file_path(url=self.installer.fftw_url)

        self.installer.get_tar_file(url=self.installer.fftw_url)
        self.assertTrue(tar_file_path.is_file())

    def test_untar(self):
        """
        Tests for successful untaring
        """

        self.installer.set_install_dirs(main_dir=self.main_dir)
        tar_file_path = \
            self.installer.get_tar_file_path(url=self.installer.fftw_url)
        tar_dir = self.installer.get_tar_dir(tar_file_path)

        self.installer.get_tar_file(url=self.installer.fftw_url)
        self.installer.untar(tar_file_path)
        self.assertTrue(tar_dir.is_dir())

    def test_configure(self):
        """
        Test for successful configuring
        """

        self.installer.set_install_dirs(main_dir=self.main_dir)
        tar_file_path = \
            self.installer.get_tar_file_path(url=self.installer.fftw_url)
        tar_dir = self.installer.get_tar_dir(tar_file_path)

        self.installer.get_tar_file(url=self.installer.fftw_url)
        self.installer.untar(tar_file_path)
        config_options = dict(prefix=str(self.installer.local_dir))
        self.installer.configure(tar_dir, config_options=config_options)
        self.assertTrue(tar_dir.joinpath('config.log').is_file())

    def test_make(self):
        """
        Test for successful making
        """

        self.installer.set_install_dirs(main_dir=self.main_dir)
        tar_file_path = \
            self.installer.get_tar_file_path(url=self.installer.fftw_url)
        tar_dir = self.installer.get_tar_dir(tar_file_path)

        self.installer.get_tar_file(url=self.installer.fftw_url)
        self.installer.untar(tar_file_path)
        config_options = dict(prefix=str(self.installer.local_dir))
        self.installer.configure(tar_dir, config_options=config_options)
        self.installer.make(tar_dir)
        bin_file = self.installer.local_dir.joinpath('bin', 'fftw-wisdom')
        self.assertTrue(bin_file.is_file())


if __name__ == '__main__':
    unittest.main()

