import hashlib
import zipfile
from pathlib import Path

from pyzipper import AESZipFile

from archive_to_images.restorer import Restorer
from archive_to_images.transformer import Transformer


def test_unprotected_archive(fs):
    """
    Fake filesystem environment creation
    """
    folder = "test_folder"
    file_prefix = "test_file"
    fs.create_dir(folder)
    for i in range(0, 10):
        file_path = f"{folder}/{file_prefix}_{i}.txt"
        fs.create_file(file_path, contents=f"This is element {i}")

    """
    Trasforming archive into images
    """
    collection = "test_collection"
    Transformer([folder], collection, 1024).process()
    assert Path(collection).exists()

    """
    Restorering archive from images
    """
    Restorer([collection]).process()

    """
    Extracting archive
    """
    extract_folder = "tmp"
    with zipfile.ZipFile(f"{collection}.zip", "r") as file:
        file.extractall(extract_folder)

    """
    Data verification
    """
    for i in range(0, 10):
        hashlib.sha512(
            open(f"{folder}/{file_prefix}_{i}.txt", "rb").read()
        ).hexdigest() == hashlib.sha512(
            open(f"{extract_folder}/{folder}/{file_prefix}_{i}.txt", "rb").read()
        ).hexdigest()


def test_protected_archive(fs):
    """
    Fake filesystem environment creation
    """
    folder = "test_folder"
    file_prefix = "test_file"
    fs.create_dir(folder)
    for i in range(0, 10):
        file_path = f"{folder}/{file_prefix}_{i}.txt"
        fs.create_file(file_path, contents=f"This is element {i}")

    """
    Trasforming archive into images
    """
    password = "P4$$w0rd000!"
    collection = "test_collection"
    Transformer([folder], collection, 1024, password).process()
    assert Path(collection).exists()

    """
    Restorering archive from images
    """
    Restorer([collection]).process()

    """
    Extracting archive
    """
    extract_folder = "tmp"
    with AESZipFile(f"{collection}.zip") as file:
        file.setpassword(password.encode("UTF-8"))
        file.extractall(extract_folder)

    """
    Data verification
    """
    for i in range(0, 10):
        hashlib.sha512(
            open(f"{folder}/{file_prefix}_{i}.txt", "rb").read()
        ).hexdigest() == hashlib.sha512(
            open(f"{extract_folder}/{folder}/{file_prefix}_{i}.txt", "rb").read()
        ).hexdigest()
