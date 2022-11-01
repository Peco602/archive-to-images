"""Restorer module"""


from typing import Dict, List, Tuple

from PIL import Image, UnidentifiedImageError
from rich.progress import Progress

from archive_to_images.processor import Processor


class Restorer(Processor):
    """
    Restorer class
    """

    def __init__(self, paths, verbose=False):
        """
        Restorer class constructor
        """
        super().__init__(paths, verbose)
        self._image_mapping: Dict[str, List[Tuple[int, str, int]]] = {}

    def _initialize(self) -> None:
        """
        Initializes the restorer before a conversion.
        """
        self._info("Restorer initialization")
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
        self._info("Scanning input files")
        task_scanning_input_files = self._add_progress_task(
            bar_text="Scanning", total_iterations=len(self._file_set)
        )
        for file in self._file_set:
            self._debug(f"Scanning file: {file}")
            try:
                image = Image.open(file).convert("L")
            except UnidentifiedImageError:
                self._warning(f"Skipping file: {file} - Not an image")
                continue

            if self._NAME_TAG in image.info:
                collection_name = image.info[self._NAME_TAG]
                index = image.info[self._INDEX_TAG]
                padding = image.info[self._PADDING_TAG]
            else:
                self._warning(f"Skipping file: {file} - No metadata")
                continue

            item = (int(index), file, int(padding))
            if collection_name not in self._image_mapping:
                self._image_mapping[collection_name] = [item]
            else:
                self._image_mapping[collection_name].append(item)

            self._update_progress_task(
                progress_task=task_scanning_input_files, advance=1
            )

    def _restore_archive(self):
        """
        Restores archive from images binary data
        """
        self._info("Restoring archives")
        task_restoring_archives = self._add_progress_task(
            bar_text="Restoring", total_iterations=len(self._file_set)
        )

        for collection_name in self._image_mapping.keys():
            self._debug(f"Restoring collection f{collection_name}")
            restored_archive_name = collection_name + self._ARCHIVE_EXT
            self._image_mapping[collection_name] = sorted(
                self._image_mapping[collection_name]
            )

            with open(restored_archive_name, "wb") as binary_file:
                for item in self._image_mapping[collection_name]:
                    image_file = item[1]
                    self._debug(f"Collecting data from image f{image_file}")
                    image = Image.open(image_file).convert("L")
                    image_data = list(Image.Image.getdata(image))
                    target_bytes = bytearray(image_data[: -item[2]])
                    immutable_bytes = bytes(target_bytes)
                    binary_file.write(immutable_bytes)
                    self._update_progress_task(
                        progress_task=task_restoring_archives, advance=1
                    )

    def process(self):
        """
        Performs th.e conversion from images to archive
        """
        self._info("Started restorer processing")
        with Progress() as self._progress:
            self._initialize()
            self._collect_input_files()
            self._scan_input_files()
            self._restore_archive()
