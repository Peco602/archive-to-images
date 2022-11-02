# Archive-To-Images

<div align="center">

[![Build status](https://github.com/Peco602/archive-to-images/workflows/build/badge.svg?branch=main&event=push)](https://github.com/Peco602/archive-to-images/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/archive-to-images.svg)](https://pypi.org/project/archive-to-images/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/Peco602/archive-to-images/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/Peco602/archive-to-images/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/Peco602/archive-to-images/releases)
[![License](https://img.shields.io/github/license/Peco602/archive-to-images)](https://github.com/Peco602/archive-to-images/blob/main/LICENSE)
![Coverage Report](https://raw.githubusercontent.com/Peco602/archive-to-images/dev/assets/images/coverage.svg)

**Archive-To-Images** is a Python CLI to transform archives into images and reverse.

</div>


## Installation

The package can be easily installed via `pip` package manager:

```
pip install archive-to-images
```


## Usage as CLI

Create an image collection from data contained in multiple paths multiple paths.

```
archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE
```

Set the maximum image size in MB (default: 1):

```
archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE -s 5
```

Encrypte the data with a password:

```
archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE -s 5 -e
```


## Usage as docker


## Buy me a coffee

Do you like my work or did you find it useful?

<a href="https://www.buymeacoffee.com/peco602" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


## License

Copyright (c) 2022-present [Giovanni Pecoraro](https://github.com/Peco602)

Licensed under [MIT License](https://github.com/Peco602/archive-to-images/blob/main/LICENSE)
