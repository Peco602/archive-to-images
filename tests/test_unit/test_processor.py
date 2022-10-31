from archive_to_images.processor import Processor


def test_initialize():
    processor = Processor(files=["."])
    processor._initialize()
    assert len(processor._file_set) == 0


def test_collect_input_files(fs):
    """
    Fake filesystem environment creation
    """
    file_set = set()
    folder = "test_folder"
    file_prefix = "test_file"
    fs.create_dir(folder)
    for i in range(0, 10):
        file_path = f"{folder}/{file_prefix}_{i}.txt"
        file_set.add(file_path)
        fs.create_file(file_path, contents=f"This is element {i}")

    """
    Temporary archive creation
    """
    processor = Processor([folder])
    processor._collect_input_files()

    """
    Collected files verification
    """
    processor._file_set = file_set
