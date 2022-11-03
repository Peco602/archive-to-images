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


## Intro

Since some cloud providers offer free unlimited picture-only storage, the **Archive-To-Images** library allows to convert any collection of files into pictures to be uploaded without any additional cost. 


## Installation

The package can be easily installed via `pip` package manager:

```bash
$ pip install archive-to-images
```

## Usage as CLI

### Transform to images

```bash
$ archive-to-images transform --help

 Usage: archive-to-images transform [OPTIONS]                                                                           
                                                                                                                        
 Transforms an archive into multiple images.                                                                            
                                                                                                                        
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --path     -p      TEXT            Path containing data to be archived. [default: None] [required]                │
│ *  --name     -n      TEXT            Name of the archive. [default: None] [required]                                │
│    --size     -s      [0.5|1|2|5|10]  Maximum size of an image in MB. [default: 1]                                   │
│    --encrypt  -e                      Protect archive with password.                                                 │
│    --verbose  -v                      Enable verbose output.                                                         │
│    --help                             Show this message and exit.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Create an image collection from data contained in multiple paths.

```bash
$ archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE
```

Set the maximum image size in MB (default: 1):

```bash
$ archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE -s 5
```

Encrypt data with a password:

```bash
$ archive-to-images transform --path /home/alice/Desktop --path /home/alice/Documents --name ARCHIVE_ALICE -s 5 -e
```

### Restore from images

```bash
$ archive-to-images restore --help

 Usage: archive-to-images restore [OPTIONS]                                                                             
                                                                                                                        
 Restores an archive from multiple images.                                                                              
                                                                                                                        
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --path     -p      TEXT  Path containing images to be processed. [default: None] [required]                       │
│    --verbose  -v            Enable verbose output.                                                                   │
│    --help                   Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Restore the archives stored in image collections:

```bash
$ archive-to-images restore --path /home/alice/Downloads/Album1 --path /home/alice/Downloads/Album2
```

The library will automatically find all the archives stored in the images and will output a `zip` archive for each one.


## Usage as docker

Run the docker image and bind the current folder to the `workspace` path inside the container:

```bash
$ docker run -it --rm -v $(pwd):/workspace peco602/archive_to_images:latest bash
```

then it is possible to use the CLI directly from the container bash.


## Buy me a coffee

Do you like my work or did you find it useful?

<a href="https://www.buymeacoffee.com/peco602" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


## License

Copyright (c) 2022-present [Giovanni Pecoraro](https://github.com/Peco602)

Licensed under [MIT License](https://github.com/Peco602/archive-to-images/blob/main/LICENSE)
