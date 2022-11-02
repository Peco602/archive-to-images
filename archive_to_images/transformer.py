"""Transformer module"""


from typing import Optional, Tuple

import math
import os
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from pyzipper import WZ_AES, ZIP_LZMA, AESZipFile
from rich.progress import Progress

from archive_to_images.processor import Processor


class Transformer(Processor):
    """
    Transformer class
    """

    def __init__(
        self, paths, collection_name, image_size, password=None, verbose=False
    ):
        """
        Transformer class constructor
        """
        super().__init__(paths, verbose)
        self._label = collection_name
        self._chunk_size = image_size
        self._archive_password = password

    def _initialize(self) -> None:
        """
        Initializes the transformer before a conversion.
        """
        self._info(f"Transformer initialization")
        super()._initialize()
        self._chunk_index = 0
        self._archive_file = NamedTemporaryFile().name

    def _collect_input_files(self) -> None:
        """
        Collects input files via directory walking.
        """
        super()._collect_input_files()

    def _create_archive(self) -> None:
        """
        Creates a zip archive from input file
        """
        self._info(f"Creating temporary archive {self._archive_file}")

        iterations = len(self._file_set)
        task_create_archive = self._add_progress_task(
            bar_text="Archiving", total_iterations=iterations
        )

        if self._archive_password:
            self._debug("Creating protected zip file")
            zip = AESZipFile(
                self._archive_file, "w", compression=ZIP_LZMA, encryption=WZ_AES
            )
            zip.setpassword(self._archive_password.encode("UTF-8"))
        else:
            self._debug("Creating unprotected zip file")
            zip = ZipFile(self._archive_file, "w")

        for file in self._file_set:
            self._debug(f"Adding file {file} to temporary archive {self._archive_file}")
            zip.write(file)
            self._update_progress_task(progress_task=task_create_archive, advance=1)

        zip.close()

    def _transform_archive(self) -> None:
        """
        Splits the archive in multiple chunks and transforms them into images
        """
        self._info("Archive transformation")
        with open(self._archive_file, mode="rb") as f:
            iterations = int(Path(self._archive_file).stat().st_size / self._chunk_size)
            task_transform_archive = self._add_progress_task(
                bar_text="Chunking", total_iterations=iterations
            )
            chunk = f.read(self._chunk_size)
            while chunk:
                _ = self._transform_chunk(chunk)
                self._chunk_index = self._chunk_index + 1
                self._update_progress_task(
                    progress_task=task_transform_archive, advance=1
                )
                chunk = f.read(self._chunk_size)

            self._debug("Removing temporary files")
            os.remove(self._archive_file)

    def _transform_chunk(self, chunk_data: bytes) -> str:
        """Transforms a data chunk into an image

        Args:
            chunk_data (bytes): List of data bytes.

        Returns:
            str: Created image filename
        """
        chunk_size: int = len(chunk_data)
        (width, height, padding) = Transformer.get_image_size(chunk_size)
        image: Image = Image.new("L", (width, height))
        image.putdata(chunk_data)

        metadata: PngInfo = PngInfo()
        metadata.add_text(self._NAME_TAG, self._label)
        metadata.add_text(self._INDEX_TAG, str(self._chunk_index))
        metadata.add_text(self._PADDING_TAG, str(padding))

        image_name: str = (
            self._label + os.sep + str(uuid.uuid1()) + self._IMAGE_EXTENSION
        )
        os.makedirs(os.path.dirname(image_name), exist_ok=True)
        image.save(image_name, pnginfo=metadata)
        self._debug(f"Created chunk image {image_name}")

        return image_name

    @staticmethod
    def get_image_size(
        data_length: int, width: Optional[int] = None
    ) -> Tuple[int, int, int]:
        """Gets the size and the padding for the chunk image

        Args:
            data_length (int): Input data length.
            width (int): Image selected width

        Returns:
            Tuple[int, int, int]: (height, width, padding)
        """
        # source Malware images: visualization and automatic classification by L. Nataraj
        # url : http://dl.acm.org/citation.cfm?id=2016908

        if width is None:  # with don't specified any with value
            if data_length < 10240:
                width = 32
            elif 10240 <= data_length <= 10240 * 3:
                width = 64
            elif 10240 * 3 <= data_length <= 10240 * 6:
                width = 128
            elif 10240 * 6 <= data_length <= 10240 * 10:
                width = 256
            elif 10240 * 10 <= data_length <= 10240 * 20:
                width = 384
            elif 10240 * 20 <= data_length <= 10240 * 50:
                width = 512
            elif 10240 * 50 <= data_length <= 10240 * 100:
                width = 768
            else:
                width = 1024

            height = int(data_length / width) + 1

        else:
            width = int(math.sqrt(data_length)) + 1
            height = width

        padding = height * width - data_length
        return (width, height, padding)

    def process(self) -> None:
        """
        Performs the conversion from archive to images
        """
        self._info("Started transformer processing")
        with Progress() as self._progress:
            self._initialize()
            self._collect_input_files()
            self._create_archive()
            self._transform_archive()
