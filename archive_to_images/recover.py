"""Recover module"""


from typing import Dict, List, Tuple

import logging

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
        self._image_mapping: Dict[str, List[Tuple[int, str, int]]] = {}

    def _initialize(self) -> None:
        """
        Initializes the recover before a conversion.
        """
        logging.info("Recover initialization")
        super()._initialize()
        self._image_mapping = {}

    def _collect_input_files(self) -> None:
        """
        Collects input files via directory walking.
        """
        super()._collect_input_files()

    def _scan_input_files(self):
        """
        Analyses all input files for archive reconstruction.
        """
        logging.info("Scanning input files")
        for file in self._file_set:
            logging.debug(f"Scanning file {file}")
            image = Image.open(file).convert("L")

            collection_name = image.info[self._NAME_TAG]
            index = image.info[self._INDEX_TAG]
            padding = image.info[self._PADDING_TAG]

            item = (int(index), file, int(padding))
            if collection_name not in self._image_mapping:
                self._image_mapping[collection_name] = [item]
            else:
                self._image_mapping[collection_name].append(item)

    def _restore_archive(self):
        """
        Restores archive from images binary data
        """
        logging.info("Restoring archives")
        for collection_name in self._image_mapping.keys():
            logging.debug(f"Restoring collection f{collection_name}")
            restored_archive_name = collection_name + self._ARCHIVE_EXT
            self._image_mapping[collection_name] = sorted(
                self._image_mapping[collection_name]
            )

            with open(restored_archive_name, "wb") as binary_file:
                for item in self._image_mapping[collection_name]:
                    image_file = item[1]
                    logging.debug(f"Collecting data from image f{image_file}")
                    image = Image.open(image_file).convert("L")
                    image_data = list(Image.Image.getdata(image))
                    target_bytes = bytearray(image_data[: -item[2]])
                    immutable_bytes = bytes(target_bytes)
                    binary_file.write(immutable_bytes)

    def process(self):
        """
        Performs the conversion from images to archive
        """
        logging.info("Started recover processing")
        self._initialize()
        self._collect_input_files()
        self._scan_input_files()
        self._restore_archive()
