from pathlib import Path
from src.Installer import Installer


class HDF5Installer(Installer):
    """
    Installer object for installing HDF5
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 log_path=None,
                 overwrite_on_exist=False):
        """
        Gets the HDF5 version, sets the HDF5 url and calls the super constructor

        Parameters
        ----------
        config_path : Path or str
            The path to the configure file
        log_path : None or Path or str
            Path to the log file containing the log of Installer.
            If None, the log will directed to stderr
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        self.overwrite_on_exist = overwrite_on_exist

        super().__init__(config_path=config_path, log_path=log_path)

        self.hdf5_version = self.config['versions']['hdf5']
        hdf5_major_minor_version = '.'.join(self.hdf5_version.split('.')[:2])
        self.hdf5_url = (f'https://support.hdfgroup.org/ftp/HDF5/releases/'
                         f'hdf5-{hdf5_major_minor_version}/'
                         f'hdf5-{self.hdf5_version}/src/'
                         f'hdf5-{self.hdf5_version}.tar.gz')
        self.file_from_make = self.local_dir.joinpath('bin', 'h5c++')

        self.extra_config_options = {'enable-cxx': 'yes'}

    def install(self):
        """
        Installs the HDF5 package
        """

        self.install_package(url=self.hdf5_url,
                             file_from_make=self.file_from_make,
                             overwrite_on_exist=self.overwrite_on_exist,
                             extra_config_option=self.extra_config_options)