from typing import Optional, Sequence, Tuple
from .folder import Folder
from .image_name_formatter import ImageNameFormatter


class CurrentImageTracker():
    """A class for keeping track of the current image in an album folder.
    (the last image captured to the album)

    The reason this task is dificult is that images in the folder
    might be deleted at any time.

    """

    def __init__(self,
                 album_folder: Folder,
                 images_folder: Folder,
                 image_name_formatter: ImageNameFormatter,
                 allowed_file_extensions: Sequence[str] = (".jpg", ".png"),
                 image_number_filename: str = ".image_number.txt") -> None:
        self.album_folder: Folder = album_folder
        self.images_folder: Folder = images_folder
        self.image_number_filename: str = image_number_filename
        self.image_name_formatter: ImageNameFormatter = image_name_formatter
        self.allowed_file_extensions: Sequence[str] = allowed_file_extensions

        self.__create_image_number_file_if_not_exists()

    def get_next_image_name(self, file_extension: str) -> str:
        next_image_number = self.__get_current_image_number() + 1
        return self.image_name_formatter.format_name(next_image_number, file_extension)

    def increase_image_number(self) -> None:
        self.__write_image_number_file(self.__get_current_image_number() + 1)

    def get_name_of_last_image(self) -> Optional[str]:
        current_image_number = self.__get_current_image_number()
        if current_image_number == 0:
            return None

        for extension in self.allowed_file_extensions:
            possible_filename = self.image_name_formatter.format_name(current_image_number, extension)
            if self.images_folder.file_exists_in_folder(possible_filename):
                return possible_filename

        raise RuntimeError(
            "Last image did not have one of allowed file extensions " + str(self.allowed_file_extensions)
        )

    def __create_image_number_file_if_not_exists(self) -> None:
        if not self.album_folder.file_exists_in_folder(self.image_number_filename):
            self.album_folder.write_file_in_folder(self.image_number_filename, "0")

    def __write_image_number_file(self, image_number: int) -> None:
        self.album_folder.write_file_in_folder(".image_number.txt", str(image_number))

    def __read_image_number_file(self) -> int:
        return int(self.album_folder.read_file_in_folder(".image_number.txt"))

    def __get_current_image_number(self) -> int:
        self.__create_image_number_file_if_not_exists()
        self.__ensure_image_number_file_correct()
        return self.__read_image_number_file()

    def __ensure_image_number_file_correct(self) -> None:
        if not self.__image_number_file_correct():
            self.__recreate_image_number_file()

    def __image_number_file_correct(self) -> bool:
        image_number = self.__read_image_number_file()
        if not self.__image_with_image_number_exists(image_number):
            return False

        next_image_number = image_number + 1
        if self.__image_with_image_number_exists(next_image_number):
            return False

        return True

    def __image_with_image_number_exists(self, image_number: int) -> bool:
        for extension in self.allowed_file_extensions:
            if self.__image_with_number_and_extension_exists(image_number, extension):
                return True

        return False

    def __image_with_number_and_extension_exists(self, image_number: int, extension: str) -> bool:
        possible_file_name = self.image_name_formatter.format_name(image_number, extension)

        if self.images_folder.file_exists_in_folder(possible_file_name):
            return True
        return False

    def __recreate_image_number_file(self) -> None:
        """Recreates the image number file based on the image files present"""
        image_names = self.images_folder.get_sorted_folder_contents()
        if not image_names:
            image_number = 0
        else:
            last_name = image_names[-1]
            image_number = self.__get_image_number_from_filename(last_name)

        self.__write_image_number_file(image_number)

    def __get_image_number_from_filename(self, filename: str) -> int:
        """Example: if the name is image_0042.png, should return 42"""
        return int(filename.split(".")[0][-4:])
