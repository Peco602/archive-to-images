import hashlib
import zipfile
from pathlib import Path

from archive_to_images.recover import Recover
from archive_to_images.transformer import Transformer


def test_create_file(fs):
    """
    Creation of the fake file system environment
    """
    folder = "/test"
    fs.create_dir(folder)
    for i in range(0, 10):
        fs.create_file(f"{folder}/test{i}.txt", contents=f"This is element {i}")

    """
    Trasforming archive into images
    """
    Transformer(["/test"], "collection", 1024).process()

    """
    Recovering archive from images
    """
    Recover("/collection").process()
    assert Path("/recovered_collection").exists()

    """
    Extracting archive
    """
    with zipfile.ZipFile("/recovered_collection", "r") as zip_ref:
        zip_ref.extractall("/tmp")

    """
    Data verification
    """
    for i in range(0, 10):
        hashlib.sha512(
            open(f"/test/test{i}.txt", "rb").read()
        ).hexdigest() == hashlib.sha512(
            open(f"/tmp/test/test{i}.txt", "rb").read()
        ).hexdigest()
