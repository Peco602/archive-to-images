import hashlib
import zipfile
from pathlib import Path

import pytest

from archive_to_images.transformer import Transformer


def test_instantiation():
    files = ["."]
    collection_name = "test_collection"
    image_size = 1024
    transformer = Transformer(
        files=files, collection_name=collection_name, image_size=image_size
    )
    assert transformer._input_files == files
    assert transformer._label == collection_name
    assert transformer._chunk_size == image_size


def test_initialize():
    transformer = Transformer(
        files=["."], collection_name="test_collection", image_size=1024
    )
    transformer._initialize()
    assert transformer._chunk_index == 0
    assert len(transformer._file_set) == 0
    assert transformer._archive_file


def test_create_archive(fs):
    transformer = Transformer(None, None, 0)
    transformer._initialize()

    """
    Fake filesystem environment creation
    """
    folder = "test_folder"
    file_prefix = "test_file"
    fs.create_dir(folder)
    for i in range(0, 10):
        file_path = f"{folder}/{file_prefix}_{i}.txt"
        transformer._file_set.add(file_path)
        fs.create_file(file_path, contents=f"This is element {i}")

    """
    Temporary archive creation
    """
    transformer._create_archive()
    assert Path(transformer._archive_file).exists()

    """
    Temporary archive extraction
    """
    extraction_folder = "tmp"
    with zipfile.ZipFile(transformer._archive_file, "r") as zip_ref:
        zip_ref.extractall(extraction_folder)

    """
    Data verification
    """
    for i in range(0, 10):
        hashlib.sha512(
            open(f"{folder}/{file_prefix}_{i}.txt", "rb").read()
        ).hexdigest() == hashlib.sha512(
            open(f"{extraction_folder}/{folder}/{file_prefix}_{i}.txt", "rb").read()
        ).hexdigest()


@pytest.mark.parametrize(
    ("data_length", "width", "expected"),
    [
        (100, None, (32, 4, 28)),
    ],
)
def test_get_image_size(data_length, width, expected):
    assert Transformer.get_image_size(data_length, width) == expected


def test_transform_chunk(fs):
    transformer = Transformer(None, "test_collection", 0)
    transformer._initialize()
    image_name = transformer._transform_chunk(chunk_data=b"\x00" * 100)
    assert Path(image_name).exists()
