import subprocess
import multiprocessing

from pathlib import Path


class BoutInstall(object):
    """
    Installation object for installing dependencies needed for the CELMA code.

    Supports the installation of the following software:
        * gcc
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

        self.mpi_version = '3.2'

        # Hdf5
        self.hdf5_version = '1.10.1'

        # Depends on hdf5
        self.netcdf_version = '4.4.1.1'
        self.netcdf_cxx_version = '4.4.1.1'

        # For plotting
        self.ffmpeg_version = '3.1.4'
        self.yasm_version = '1.3.0'
        self.nasm_version = '2.13.01'

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
        Set the directories to install to

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
