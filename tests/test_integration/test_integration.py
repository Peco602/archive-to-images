import hashlib
import zipfile
from pathlib import Path

from archive_to_images.recover import Recover
from archive_to_images.transformer import Transformer


def test_create_file(fs):
    """
    Creation of the fake file system environment
    """
    test_folder = "test"
    fs.create_dir(test_folder)
    for i in range(0, 10):
        fs.create_file(f"{test_folder}/test{i}.txt", contents=f"This is element {i}")

    """
    Trasforming archive into images
    """
    Transformer([test_folder], "collection", 1024).process()
    assert Path("collection").exists()

    """
    Recovering archive from images
    """
    Recover(["collection"]).process()

    """
    Extracting archive
    """
    tmp_folder = "tmp"
    with zipfile.ZipFile("collection.zip", "r") as zip_ref:
        zip_ref.extractall(tmp_folder)

    """
    Data verification
    """
    for i in range(0, 10):
        hashlib.sha512(
            open(f"/{test_folder}/test{i}.txt", "rb").read()
        ).hexdigest() == hashlib.sha512(
            open(f"/{tmp_folder}/{test_folder}/test{i}.txt", "rb").read()
        ).hexdigest()
