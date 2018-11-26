

[![Build Status](https://travis-ci.org/CELMA-project/bout_install.svg?branch=master)](https://travis-ci.org/CELMA-project/bout_install)
[![codecov](https://codecov.io/gh/CELMA-project/bout_install/branch/master/graph/badge.svg)](https://codecov.io/gh/CELMA-project/bout_install)
[![PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](https://github.com/CELMA-project/bout_install/blob/master/LICENSE)

* []()

# bout_install

Python package to install [BOUT++](http://boutproject.github.io) and it's 
dependencies.

> **NOTE**: This package is meant as a "last resort" to install BOUT++, for 
example when you are not a `root` user, and you are trying to install on a 
tricky system.
Othervise 
BOUT++ can easily be installed using 
[docker](https://bout-dev.readthedocs.io/en/latest/user_docs/installing.html#docker-image)
or installed as explained in the BOUT ++ [documentation](https://bout-dev.readthedocs.io/en/latest/user_docs/installing.html#installing-dependencies)
.

## Getting Started

`bout_install` is a lightweight package, and requires only `python3`, 
`requests` and an internet connection to run. 

### Installing from pip

The package can be installed from `pip`:

```
pip install bout_install
```

### Installing from source

Alternatively it can be installed from source

#### Prerequisites

The prerequisites can be installed through
[`requirements.txt`](https://pip.pypa.io/en/stable/user_guide/#requirements-files):

```
pip install -r requirements.txt
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

