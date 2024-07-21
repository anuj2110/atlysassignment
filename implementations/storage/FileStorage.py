from helpers.StorageInterface import StorageInterface
import os
import json
from pathlib import Path

class FileStorageInterface(StorageInterface):
    def __init__(self, file_path):
        self.file_path = file_path
    def save(self, data,*args):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def get_data(self):
        data = None
        with open(self.file_path,"r") as f:
            data = json.load(f)
        return data