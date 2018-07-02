import configparser
import logging
import multiprocessing
import os
import requests
import shutil
import subprocess
import tarfile
from pathlib import Path


class Installer(object):
    """
    Installation object for installing dependencies needed for the CELMA code.

    Supports the installation of the following software:
        * gcc
        * cmake
        * mpi
        * fftw
        * hdf5
        * netCDF-4
        * SLEPc
        * PETSc
        * BOUT++
        * ffpmeg
        
    Examples
    --------
    FIXME
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 log_path=None):
        """
        Sets the versions of the different software

        configparser
        FIXME

        Parameters
        ----------
        config_path : Path or str
            The path to the configure file
        log_path : None or Path or str
            Path to the log file containing the log of Installer.
            If None, the log will directed to stderr
        """

        self.config = configparser.ConfigParser(allow_no_value=True)
        with Path(config_path).open() as f:
            self.config.read_file(f)

        # Set input
        self.log_path = log_path

        # Obtain the current working directory
        self.cwd = Path.cwd()

        # Obtain install dirs
        main_dir = self.config['install_dirs']['main_dir']
        install_dir = self.config['install_dirs']['install_dir']
        local_dir = self.config['install_dirs']['local_dir']
        examples_dir = self.config['install_dirs']['examples_dir']

        self.main_dir = main_dir if main_dir != '' else None
        self.install_dir = install_dir if install_dir != '' else None
        self.local_dir = local_dir if local_dir != '' else None
        self.examples_dir = examples_dir if examples_dir != '' else None

        # Setup the install dirs
        self.setup_install_dirs(main_dir=self.main_dir,
                                install_dir=self.install_dir,
                                local_dir=self.local_dir,
                                examples_dir=self.examples_dir)

        # Set the versions
        self.gcc_version = self.config['versions']['gcc']
        self.cmake_version = self.config['versions']['cmake']
        cmake_major_minor_version = '.'.join(self.cmake_version.split('.')[:2])
        self.mpi_version = self.config['versions']['mpi']
        self.hdf5_version = self.config['versions']['hdf5']
        hdf5_major_minor_version = '.'.join(self.cmake_version.split('.')[:2])
        self.netcdf_version = self.config['versions']['netcdf']
        self.netcdf_cxx_version = self.config['versions']['netcdf_cxx']
        self.slepc_version = self.config['versions']['slepc']
        self.petsc_version = self.config['versions']['petsc']
        self.nasm_version = self.config['versions']['nasm']
        self.yasm_version = self.config['versions']['yasm']
        self.ffmpeg_version = self.config['versions']['ffmpeg']

        # Set the urls
        self.gcc_url = (f'ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/'
                        f'gcc-{self.gcc_version}/gcc-{self.gcc_version}.tar.gz')
        self.cmake_url = (f'http://cmake.org/files/'
                          f'v{cmake_major_minor_version}/'
                          f'cmake-{self.cmake_version}.tar.gz')
        self.mpi_url = (f'http://www.mpich.org/static/downloads/'
                        f'{self.mpi_version}/mpich-{self.mpi_version}.tar.gz')
        self.hdf5_url = (f'wget https://support.hdfgroup.org/ftp/HDF5/releases/'
                         f'hdf5-{hdf5_major_minor_version}/'
                         f'hdf5-{self.hdf5_version}/src/'
                         f'hdf5-{self.hdf5_version}.tar.gz')
        self.netcdf_cxx_url = (f'http://github.com/Unidata/netcdf-cxx4/archive/'
                               f'v{self.netcdf_cxx_version}.tar.gz')
        self.slepc_url = (f'http://slepc.upv.es/download/download.php?'
                          f'filename=slepc-{self.slepc_version}.tar.gz')
        self.petsc_url = (f'http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/'
                          f'petsc-{self.petsc_version}.tar.gz')
        self.bout_url = (f'')
        self.nasm_url = (f'http://www.nasm.us/pub/nasm/releasebuilds/' 
                         f'{self.nasm_version}/'
                         f'nasm-{self.nasm_version}.tar.gz')
        self.yasm_url = (f'http://www.tortall.net/projects/yasm/releases/yasm-'
                         f'{self.yasm_version}.tar.gz')
        self.ffmpeg_url = (f'http://ffmpeg.org/releases/'
                           f'ffmpeg-{self.ffmpeg_version}.tar.bz2')

        # Declare other class variables
        self.logger = None

        # Setup the logger
        self._setup_logger()

    def _setup_logger(self):
        """
        Sets up the logger instance.
        """
        formatter = logging.Formatter('[{asctime}][{levelname:<7}] {message}',
                                      style='{')

        if self.log_path is not None:
            log_path = Path(self.log_path).absolute()
            log_dir = log_path.parent
            log_dir.mkdir(exist_ok=True, parents=True)
            handler = logging.FileHandler(str(log_path))
        else:
            handler = logging.StreamHandler()

        handler.setFormatter(formatter)

        self.logger = logging.getLogger('bout_install')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def setup_install_dirs(self,
                           main_dir=None,
                           install_dir=None,
                           local_dir=None,
                           examples_dir=None):
        """
        Set the install directories for the packages

        Parameters
        ----------
        main_dir : None or str or Path
            The super directory of install_dir, local_dir and example_dir
            (if not set).
            If None, the home directory will be used.
            install_dir, local_dir and example_dir have precedence over main_dir
        install_dir : None or str or Path
            The directory to put the files to install from.
             If None, the directory will be made under main_dir
        local_dir : None or str or Path
            The directory to put the installed files.
             If None, the directory will be made under main_dir
        examples_dir : None or str or Path
            The directory to put the examples (needed for installing ffmpeg).
            If None, the directory will be made under main_dir
        """

        if main_dir is None:
            self.main_dir = Path(__file__).home().absolute()
        else:
            self.main_dir = Path(main_dir).absolute()

        if install_dir is None:
            self.install_dir = self.main_dir.joinpath('install')
        else:
            self.install_dir = Path(install_dir).absolute()

        if local_dir is None:
            self.local_dir = self.main_dir.joinpath('local')
        else:
            self.local_dir = Path(local_dir).absolute()

        if examples_dir is None:
            self.examples_dir = self.main_dir.joinpath('examples')
        else:
            self.examples_dir = Path(examples_dir).absolute()

        # Make the directories
        if not (install_dir is None and
                local_dir is None and
                examples_dir is None):
            self.main_dir.mkdir(parents=True, exist_ok=True)

        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.local_dir.mkdir(parents=True, exist_ok=True)
        self.examples_dir.mkdir(parents=True, exist_ok=True)

    def get_tar_file(self, url):
        """
        Obtain a tar file from url

        Parameters
        ----------
        url : str
            The url to get the tar file from
        """

        response = requests.get(url, stream=True)
        response.raise_for_status()

        tar_file_path = self.get_tar_file_path(url)

        with tar_file_path.open('wb') as f:
            shutil.copyfileobj(response.raw, f)

    def get_tar_file_path(self, url):
        """
        Returns the path to the tar file

        Parameters
        ----------
        url : str
            The url to get the tar file from

        Returns
        -------
        tar_file_path : Path
            The path to the tar file
        """

        # The file name is the last part of the url
        file_name = url.split('/')[-1]
        tar_file_path = self.install_dir.joinpath(file_name)
        return tar_file_path

    @staticmethod
    def untar(tar_path):
        """
        Untar a tar file

        Parameters
        ----------
        tar_path : str or Path
            Tar file to extract
        """

        tar_path = Path(tar_path).absolute()
        tar_extract_dir = tar_path.parent

        tar = tarfile.open(tar_path)
        tar.extractall(path=tar_extract_dir)
        tar.close()

    @staticmethod
    def get_tar_dir(tar_path):
        """
        Returns the path to the tar directory (directory of untarred files)

        Parameters
        ----------
        tar_path : str or Path
            Path to tar file

        Returns
        -------
        tar_dir : Path
            The untarred directory
        """
        tar_dir = Path(tar_path).absolute().with_suffix('').with_suffix('')
        return tar_dir

    def configure(self, path, config_options=None):
        """
        Configure the package

        Parameters
        ----------
        path : Path or str
            Path to the config file
        config_options : dict
            Configuration options to use with `./configure`
            The configuration options will be converted to `--key=val` during
            runtime
        """

        os.chdir(path)

        options = ''
        if config_options is not None:
            for key, val in config_options.items():
                options += f' --{key}={val}'

        config_str = f'./configure{options}'

        result = subprocess.run(config_str.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        os.chdir(self.cwd)
        if result.returncode != 0:
            self._spawn_subprocess(result)

    def make(self, path):
        """
        Make the package

        Parameters
        ----------
        path : Path or str
            Path to the configure file
        """

        os.chdir(path)

        make_str = 'make'

        result = subprocess.run(make_str.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        result.check_returncode()

        make_install_str = 'make install'

        result = subprocess.run(make_install_str.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        result.check_returncode()

        os.chdir(self.cwd)

    def install_package(self,
                        url,
                        file_from_make,
                        overwrite_on_exist=False,
                        extra_config_option=None):
        """
        Installs a package if it's not installed

        Parameters
        ----------
        url : str
            Url to the tar file of the package
        file_from_make : Path or str
            File originating from the make processes (used to check if the
            package has been made)
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        extra_config_option : dict
            Configure option to include.
            --prefix=self.local_dir is already added as an option
        """

        tar_file_path = self.get_tar_file_path(url)
        tar_dir = self.get_tar_dir(tar_file_path)
        config_log_path = tar_dir.joinpath('config.log')

        if not tar_file_path.is_file() or overwrite_on_exist:
            self.logger.info(f'{tar_file_path} not found, downloading')
            self.get_tar_file(url)
        else:
            self.logger.info(f'{tar_file_path} found, skipping download')

        if not tar_dir.is_dir() or overwrite_on_exist:
            self.logger.info(f'{tar_dir} not found, untarring')
            self.untar(tar_file_path)
        else:
            self.logger.info(f'{tar_dir} found, skipping untarring')

        if not config_log_path.is_file() or overwrite_on_exist:
            self.logger.info(f'{config_log_path} not found, configuring')
            config_options = dict(prefix=str(self.local_dir))
            if extra_config_option is not None:
                config_options = {**config_options, **extra_config_option}
            self.configure(tar_dir, config_options=config_options)
        else:
            self.logger.info(f'{tar_dir} found, skipping untarring')

        if not file_from_make.is_file() or overwrite_on_exist:
            self.logger.info(f'{file_from_make} not found, running make')
            self.make(tar_dir)
        else:
            self.logger.info(f'{file_from_make} found, skipping making')

    def _spawn_subprocess(self, result):
        """
        Raises errors from the subprocess in a clean way

        Parameters
        ----------
        result : subprocess.CompletedProcess
            The result from the subprocess
        """

        self.logger.error('Subprocess failed with stdout:')
        self.logger.error(result.stdout)
        self.logger.error('and stderr:')
        self.logger.error(result.stderr)

        result.check_returncode()

# FIXME: Multiprocess: One process kills all on error, and error is logged
# FIXME: x264 from git (needed for ffmpeg)
# FIXME: BOUT++ from git
# FIXME: netcdf depends on hdf5
# FIXME: prepend wget --no-check-certificate to cmake
# FIXME: gfortran as a dependency?
# FIXME: Update README
