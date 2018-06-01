import os
import shutil
import requests
import multiprocessing
import subprocess
import tarfile
from pathlib import Path


class BoutInstall(object):
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

    def __init__(self):
        """
        Sets the versions of the different software
        FIXME
        """

        # Obtain the current working directory
        self.cwd = Path.cwd()

        # Set the versions
        self.gcc_version = '6.1.0'
        cmake_major_minor_version = '3.7'
        self.cmake_version = f'{cmake_major_minor_version}.2'
        self.mpi_version = '3.2'
        self.fftw_version = '3.3.6-pl2'
        hdf5_major_minor_version = '1.10'
        self.hdf5_version = f'{hdf5_major_minor_version}.1'
        self.netcdf_version = '4.4.1.1'
        self.netcdf_cxx_version = '4.4.1.1'
        self.slepc_version = '3.4.4'
        self.petsc_version = '3.4.5'
        self.nasm_version = '2.13.01'
        self.yasm_version = '1.3.0'
        self.ffmpeg_version = '3.1.4'

        # Set the urls
        self.gcc_url = (f'ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/'
                        f'gcc-{self.gcc_version}/gcc-{self.gcc_version}.tar.gz')
        self.cmake_url = (f'http://cmake.org/files/'
                          f'v{cmake_major_minor_version}/'
                          f'cmake-{self.cmake_version}.tar.gz')
        self.mpi_url = (f'http://www.mpich.org/static/downloads/'
                        f'{self.mpi_version}/mpich-{self.mpi_version}.tar.gz')
        self.fftw_url = f'http://www.fftw.org/fftw-{self.fftw_version}.tar.gz'
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
        # Install dirs
        self.main_dir = None
        self.install_dir = None
        self.local_dir = None
        self.examples_dir = None

    def set_install_dirs(self,
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
            The url to get from

        Returns
        -------
        path : Path
            The path to the tar file
        """

        if self.install_dir is None:
            raise RuntimeError('The installation directory has not been set, '
                               'please run self.set_install_dirs')

        response = requests.get(url, stream=True)
        response.raise_for_status()

        # The file name is the last part of the url
        file_name = url.split('/')[-1]
        path = self.install_dir.joinpath(file_name)

        with path.open('wb') as f:
            shutil.copyfileobj(response.raw, f)

        return path

    @staticmethod
    def untar(tar_file):
        """
        Untar a tar file

        Parameters
        ----------
        tar_file : str or Path
            Tar file to extract

        Returns
        -------
        tar_dir : Path
            The untarred directory
        """

        tar_path = Path(tar_file).absolute()
        tar_extract_dir = tar_path.parent
        tar_dir = tar_path.with_suffix('').with_suffix('')

        tar = tarfile.open(tar_path)
        tar.extractall(path=tar_extract_dir)
        tar.close()

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

        # NOTE: Capturing both stdout and stderr at once, see
        # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess.stdout
        result = subprocess.run(config_str.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        os.chdir(self.cwd)
        result.check_returncode()


# FIXME: Multiprocess: One process kills all on error, and error is logged
# FIXME: x264 from git (needed for ffmpeg)
# FIXME: BOUT++ from git
# FIXME: netcdf depends on hdf5
# FIXME: prepend wget --no-check-certificate to cmake
# FIXME: gfortran as a dependency?