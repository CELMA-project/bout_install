#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from bout_install import __version__
from bout_install import __name__


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=__name__,
    version=__version__,
    author='Michael Løiten',
    author_email='michael.l.magnussen@gmail.com',
    description='Python package to install BOUT++ and its dependencies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CELMA-project/bout_install',
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.20.1'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3.0',
        'Operating System :: OS Independent',
    ],
    entry_points={'console_scripts': ['bout_install = bout_install.main:main']},
)
