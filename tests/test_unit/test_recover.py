from pathlib import Path

from PIL import Image
from PIL.PngImagePlugin import PngInfo

from archive_to_images.recover import Recover


def test_instantiation():
    files = ["."]
    recover = Recover(files=files)
    assert recover._input_files == files


def test_initialize():
    recover = Recover(files=["."])
    recover._initialize()
    assert len(recover._file_set) == 0


def test_scan_input_files(fs):
    recover = Recover(None)
    test_label = "test_collection"
    test_index = 1
    test_padding = 0
    test_height: int = 10
    test_width: int = 10
    test_data = b"\x00" * test_height * test_width

    """
    Test image creation
    """
    image_name: str = "test.png"
    assert not Path(image_name).exists()
    image: Image = Image.new("L", (test_height, test_width))
    image.putdata(test_data)
    metadata: PngInfo = PngInfo()
    metadata.add_text(recover._NAME_TAG, test_label)
    metadata.add_text(recover._INDEX_TAG, str(test_index))
    metadata.add_text(recover._PADDING_TAG, str(test_padding))
    image.save(image_name, pnginfo=metadata)
    assert Path(image_name).exists()

    """
    Test image scanning
    """
    recover._file_set.add("test.png")
    recover._scan_input_files()

    """
    Data verification
    """
    assert len(recover._image_mapping.keys()) == 1
    assert list(recover._image_mapping.keys()) == [test_label]
    assert recover._image_mapping[test_label][0][0] == test_index
    assert recover._image_mapping[test_label][0][1] == image_name
    assert recover._image_mapping[test_label][0][2] == test_padding


def test_restore_archive(fs):
    recover = Recover(None)
    test_label = "test_collection"
    test_index = 1
    test_padding = 0
    test_height: int = 10
    test_width: int = 10
    test_data = b"\x00" * test_height * test_width

    """
    Test image creation
    """
    image_name: str = "test.png"
    assert not Path(image_name).exists()
    image: Image = Image.new("L", (test_height, test_width))
    image.putdata(test_data)
    metadata: PngInfo = PngInfo()
    metadata.add_text(recover._NAME_TAG, test_label)
    metadata.add_text(recover._INDEX_TAG, str(test_index))
    metadata.add_text(recover._PADDING_TAG, str(test_padding))
    image.save(image_name, pnginfo=metadata)
    assert Path(image_name).exists()

    """
    Image mapping
    """
    recover._image_mapping = {test_label: [(test_index, image_name, test_padding)]}

    """
    Archive recovery
    """
    assert not Path(test_label + recover._ARCHIVE_EXT).exists()
    recover._restore_archive()
    assert Path(test_label + recover._ARCHIVE_EXT).exists()
