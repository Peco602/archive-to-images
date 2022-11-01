# archive-to-images

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

`archive-to-images` is a Python CLI to transform archives into images and reverse.

</div>


## Installation

The package can be easily installed via `pip` package manager:

```
pip install archive-to-images
```


## Usage

1. Create an image collection `ARCHIVE_ALICE` from multiple paths.

```
archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE
```

You can create additional image collections from other paths. 

```
archive-to-images transform --path /home/bob/Downloads --name ARCHIVE_BOB -s 5 -e
```

The maximum image size can be set via the `-s` parameter. The archived data can be optionally protected via password by adding the `-e` parameter. The password must be provided via prompt.

2. Upload the pictures to your favorite photo cloud storage to store them safely.

3. Download all the images when you need to restore your archive.

```
archive-to-images restore --path /home/alice/Downloads/
```

4. The archives will appear as `zip` files. In case of encryption the archive can be extracted via [7-Zip](https://www.7-zip.org/download.html).


## Buy me a coffee

Do you like my work or did you find it useful?

<a href="https://www.buymeacoffee.com/peco602" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


## Credits

`archive-to-images` is a Python CLI created with https://github.com/TezRomacH/python-package-template.
