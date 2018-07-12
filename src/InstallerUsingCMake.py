from src.Installer import Installer


class InstallerUsingCMake(Installer):
    """
    An Installer class which installs configures using `cmake` rather than 
    `./configure`
    """

    @staticmethod
    def get_cmake_command(cmake_options=None):
        """
        Get the command to configure the package

        Parameters
        ----------
        cmake_options : dict
            Configuration options to use with `cmake`.
            The configuration options will be converted to `--key=val` during
            runtime

        Returns
        -------
        cmake_str : str
            The configuration command
        """

        options = ''
        if cmake_options is not None:
            for key, val in cmake_options.items():
                options += f' -{key}={val}'

        cmake_str = f'cmake{options}'
        return cmake_str

    def run_configure(self,
                      tar_dir,
                      makefile_path,
                      extra_cmake_option,
                      overwrite_on_exist):
        """
        Configures the package by running CMake

        Parameters
        ----------
        tar_dir : Path
            Directory of the tar file
        makefile_path : Path
            Path to the Makefile
        extra_cmake_option:
            Configure option to include.
            -DCMAKE_INSTALL_PREFIX=self.local_dir is already added as an option
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        if not makefile_path.is_file() or overwrite_on_exist:
            # Get the CMake options
            cmake_options = dict(DCMAKE_INSTALL_PREFIX=str(self.local_dir))
            if extra_cmake_option is not None:
                cmake_options = {**cmake_options, **extra_cmake_option}

            cmake_str = self.get_cmake_command(cmake_options=cmake_options)

            build_dir = tar_dir.joinpath('build')
            # NOTE: We could get in trouble if the build_dir already exists,
            #       so we deliberately throw an error if the directory exists
            build_dir.mkdir(exist_ok=False)

            self.logger.info(f'Running cmake with: {cmake_str}')
            self.run_subprocess(cmake_str, build_dir)
        else:
            self.logger.info(f'{makefile_path} found, skipping running of '
                             f'CMake')
