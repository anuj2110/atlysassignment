from helpers.StorageInterface import StorageInterface
import os
import json
from pathlib import Path


class FileStorageInterface(StorageInterface):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data, *args):
        file_path = f"{os.environ['BASE_DIR']}/{self.file_path}"
        file_data = self.get_data()
        for key in data:
            file_data[key] = data[key]
        with open(file_path, 'w') as f:
            json.dump(file_data, f, indent=4)

    def get_data(self):
        data = None
        file_path = f"{os.environ['BASE_DIR']}/{self.file_path}"
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({}, f)
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
