"""Example of code."""


import os

from PIL import Image

from archive_to_images.processor import Processor


class Recover(Processor):
    """
    Recover class
    """

    def __init__(self, folder):
        self.folder = folder
        self.mapping = {}

    def _scan_folder(self) -> None:
        for path, _, files in os.walk(self.folder):
            for f in files:
                self._read_metadata(os.path.join(path, f))

    def _read_metadata(self, file):
        image = Image.open(file).convert("L")
        name = image.info["name"]
        index = image.info["index"]
        padding = image.info["padding"]
        if name not in self.mapping:
            self.mapping[name] = [(int(index), file, int(padding))]
        else:
            self.mapping[name].append((int(index), file, int(padding)))

    def _restore_file(self):
        for k in self.mapping.keys():
            target_name = "recovered_" + k
            target_data = []
            self.mapping[k] = sorted(self.mapping[k])
            print(self.mapping[k])
            for i in self.mapping[k]:
                # opening a  image
                print(f"adding {i[1]}")
                image = Image.open(i[1]).convert("L")
                image_data = list(Image.Image.getdata(image))
                target_data.extend(image_data[: -i[2]])

            target_bytes = bytearray(target_data)
            immutable_bytes = bytes(target_bytes)

            with open(target_name, "wb") as binary_file:
                binary_file.write(immutable_bytes)

    def process(self):
        self._scan_folder()
        self._restore_file()
