#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
from pathlib import Path
# from src.BOUTPPInstaller import BOUTPPInstaller
from src.CMakeInstaller import CMakeInstaller
from src.FFMPEGInstaller import FFMPEGInstaller
from src.FFTWInstaller import FFTWInstaller
from src.GCCInstaller import GCCInstaller
from src.HDF5Installer import HDF5Installer
from src.MPIInstaller import MPIInstaller
from src.NetCDFInstaller import NetCDFInstaller
from src.PETScInstaller import PETScInstaller
from src.SLEPcInstaller import SLEPcInstaller
from src.SundialsInstaller import SundialsInstaller


def main(config_path):
    """
    Function which installs BOUT++ with its dependencies.

    Parameters
    ----------
    config_path : str or Path
        Path to the configuration file.
        See src.config.ini for the default configuration
    """

    # FIXME: Options for adding lines to bashrc or bash_profile
    # FIXME: Why is netcdf_cxx in config.ini?

    config = configparser.ConfigParser(allow_no_value=True)
    with config_path.open() as f:
        config.read_file(f)

    if config.getboolean('optional', 'gcc'):
        # FIXME: Must have in bashrc or bash_profile
        print('Installing gcc...')
        gcc_installer = GCCInstaller(config_path=config_path)
        gcc_installer.install()
        print('..done')

    if config.getboolean('required', 'mpi'):
        print('Installing mpi...')
        mpi_installer = MPIInstaller(config_path=config_path)
        mpi_installer.install()
        print('...done')

    if config.getboolean('optional', 'cmake'):
        print('Installing cmake...')
        cmake_installer = CMakeInstaller(config_path=config_path)
        cmake_installer.install()
        print('...done')

    if config.getboolean('optional', 'ffmpeg'):
        print('Installing ffmpeg...')
        ffmpeg_installer = FFMPEGInstaller(config_path=config_path)
        ffmpeg_installer.install()
        print('...done')

    if config.getboolean('required', 'fftw'):
        print('Installing fftw...')
        fftw_installer = FFTWInstaller(config_path=config_path)
        fftw_installer.install()
        print('...done')

    if config.getboolean('required', 'hdf5'):
        print('Installing hd5...')
        hdf5_installer = HDF5Installer(config_path=config_path)
        hdf5_installer.install()
        print('...done')

    if config.getboolean('required', 'netcdf'):
        print('Installing netcdf...')
        netcdf_installer = NetCDFInstaller(config_path=config_path)
        netcdf_installer.install()
        print('...done')

    if config.getboolean('optional', 'sundials'):
        print('Installing sundials...')
        sundials_installer = SundialsInstaller(config_path=config_path)
        sundials_installer.install()
        print('...done')

    if config.getboolean('optional', 'petsc'):
        print('Installing petsc...')
        petsc_installer = PETScInstaller(config_path=config_path)
        petsc_installer.install()
        print('...done')

    if config.getboolean('optional', 'slepsc'):
        print('Installing slepc...')
        slepc_installer = SLEPcInstaller(config_path=config_path)
        slepc_installer.install()
        print('...done')

#    boutpp_installer = BOUTPPInstaller(config_path=config_path)
#    boutpp_installer.install()
#    print('...done')


if __name__ == '__main__':
    parser = \
        argparse.ArgumentParser(description='Install BOUT++ with dependencies')

    parser.add_argument('-c',
                        '--config',
                        help='Path to the configuration file. See '
                             'src/config.ini for details',
                        required=False)

    args = parser.parse_args()

    if args.config is None:
        root_dir = Path(__file__).absolute().parents[1]
        config_path = root_dir.joinpath('src', 'config.ini')
    else:
        config_path = Path(args.config)

    main(config_path)
