"""Example of code."""


from typing import Dict, List, Tuple

import logging
import os

from PIL import Image

from archive_to_images.processor import Processor


class Recover(Processor):
    """
    Recover class
    """

    def __init__(self, files):
        """
        Recover class constructor
        """
        super().__init__(files)

    def _initialize(self) -> None:
        """
        Initializes the recover before a conversion.
        """
        super()._initialize()
        self.image_mapping: Dict[str, List[Tuple[int, str, int]]] = {}

    def _collect_input_files(self) -> None:
        """
        Collects input files via directory walking.
        """
        super()._collect_input_files()

    def _scan_input_files(self):
        """
        Analyses all input files for archive reconstruction.
        """
        for file in self._file_set:
            image = Image.open(file).convert("L")

            collection_name = image.info[self._NAME_TAG]
            index = image.info[self._INDEX_TAG]
            padding = image.info[self._PADDING_TAG]

            item = (int(index), file, int(padding))
            if collection_name not in self.image_mapping:
                self.image_mapping[collection_name] = [item]
            else:
                self.image_mapping[collection_name].append(item)

    def _restore_archive(self):
        """
        Restores archive from images binary data
        """
        for collection_name in self.image_mapping.keys():
            restored_archive_name = collection_name + self._ARCHIVE_EXT
            self.image_mapping[collection_name] = sorted(
                self.image_mapping[collection_name]
            )

            with open(restored_archive_name, "wb") as binary_file:
                for item in self.image_mapping[collection_name]:
                    print(f"adding {item[1]}")
                    image = Image.open(item[1]).convert("L")
                    image_data = list(Image.Image.getdata(image))
                    target_bytes = bytearray(image_data[: -item[2]])
                    immutable_bytes = bytes(target_bytes)
                    binary_file.write(immutable_bytes)

    def process(self):
        """
        Performs the conversion from images to archive
        """
        self._initialize()
        self._collect_input_files()
        self._scan_input_files()
        self._restore_archive()
