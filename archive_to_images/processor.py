"""Processor module"""

from typing import Set

import logging
import os


class Processor:
    """
    Processor class
    """

    _ARCHIVE_EXT = ".zip"
    _NAME_TAG = "name"
    _INDEX_TAG = "index"
    _PADDING_TAG = "padding"

    def __init__(self, files):
        """
        Processor class constructor.
        """
        self._input_files = files
        self._file_set: Set[str] = set()

    def _initialize(self) -> None:
        """
        Initializes the processor before a conversion.
        """
        self._file_set = set()

    def _collect_input_files(self) -> None:
        """
        Collects input files via directory walking.
        """
        logging.info(f"Collecting input files")
        for input_file in self._input_files:
            if os.path.isdir(input_file):
                logging.debug(f"Walking directory {input_file}")
                for path, _, directory_files in os.walk(input_file):
                    for file in directory_files:
                        self._file_set.add(os.path.join(path, file))
                        logging.debug(f"Adding file {file}")
            else:
                self._file_set.add(input_file)
                logging.debug(f"Adding file {input_file}")
