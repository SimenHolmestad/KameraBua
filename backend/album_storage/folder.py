import os
import shutil
from typing import List


class Folder():
    """A class for interacting with a folder"""

    def __init__(self, base_path: str, dir_name: str) -> None:
        self.base_path = base_path
        self.dir_name = dir_name
        self.create_folder_if_not_exist()

    def get_folder_contents(self) -> List[str]:
        path_to_folder = self.get_path()
        return os.listdir(path_to_folder)

    def get_sorted_folder_contents(self) -> List[str]:
        return sorted(self.get_folder_contents())

    def get_path(self) -> str:
        return os.path.join(
            self.base_path,
            self.dir_name
        )

    def get_name(self) -> str:
        return self.dir_name

    def count_files(self) -> int:
        """Return number of files inside the folder"""
        return len(self.get_folder_contents())

    def get_path_to_file(self, filename: str) -> str:
        return os.path.join(
            self.get_path(),
            filename
        )

    def write_file_in_folder(self, filename: str, content: str) -> None:
        path_to_file = self.get_path_to_file(filename)
        with open(path_to_file, "w") as f:
            f.write(content)

    def read_file_in_folder(self, filename: str) -> str:
        path_to_file = self.get_path_to_file(filename)
        with open(path_to_file, "r") as f:
            return f.read()

    def file_exists_in_folder(self, filename: str) -> bool:
        path_to_file = self.get_path_to_file(filename)
        return os.path.exists(path_to_file)

    def remove_all_folder_content(self) -> None:
        path_to_folder = self.get_path()
        shutil.rmtree(path_to_folder)
        os.mkdir(path_to_folder)

    def create_folder_if_not_exist(self) -> None:
        if not os.path.exists(self.get_path()):
            os.makedirs(self.get_path())
