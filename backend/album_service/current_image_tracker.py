import os
import re
from typing import Optional

from .image_name_formatter import format_image_name

DEFAULT_IMAGE_NUMBER_FILENAME = ".image_number.txt"
DEFAULT_IMAGE_NAME_PREFIX = "image"


class CurrentImageTracker:
    def __init__(
        self,
        album_folder_path: str,
        images_folder_path: str,
        image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX,
        image_number_filename: str = DEFAULT_IMAGE_NUMBER_FILENAME
    ) -> None:
        self.album_folder_path = album_folder_path
        self.images_folder_path = images_folder_path
        self.image_name_prefix = image_name_prefix
        self.image_number_filename = image_number_filename

    def get_next_image_base_name(self) -> str:
        next_image_number = self._get_current_image_number() + 1
        return format_image_name(self.image_name_prefix, next_image_number)

    def increase_image_number(self) -> None:
        current_number = self._get_current_image_number()
        self._write_image_number_file(current_number + 1)

    def get_name_of_last_image(self) -> Optional[str]:
        self._get_current_image_number()
        return self._find_last_image_filename()

    def _create_image_number_file_if_not_exists(self) -> None:
        image_number_path = os.path.join(self.album_folder_path, self.image_number_filename)
        if not os.path.exists(image_number_path):
            with open(image_number_path, "w") as file_handle:
                file_handle.write("0")

    def _write_image_number_file(self, image_number: int) -> None:
        with open(os.path.join(self.album_folder_path, self.image_number_filename), "w") as file_handle:
            file_handle.write(str(image_number))

    def _read_image_number_file(self) -> int:
        with open(os.path.join(self.album_folder_path, self.image_number_filename), "r") as file_handle:
            return int(file_handle.read())

    def _get_current_image_number(self) -> int:
        self._create_image_number_file_if_not_exists()
        self._ensure_image_number_file_correct()
        return self._read_image_number_file()

    def _ensure_image_number_file_correct(self) -> None:
        if not self._image_number_file_correct():
            self._recreate_image_number_file()

    def _image_number_file_correct(self) -> bool:
        return self._read_image_number_file() == self._find_last_image_number()

    def _recreate_image_number_file(self) -> None:
        self._write_image_number_file(self._find_last_image_number())

    def _find_last_image_number(self) -> int:
        last_image = self._find_last_image_filename()
        if not last_image:
            return 0
        return self._try_get_image_number(last_image) or 0

    def _find_last_image_filename(self) -> Optional[str]:
        image_names = sorted(os.listdir(self.images_folder_path), reverse=True)
        for image_name in image_names:
            if self._try_get_image_number(image_name) is not None:
                return image_name
        return None

    def _try_get_image_number(self, filename: str) -> Optional[int]:
        pattern = f"^{re.escape(self.image_name_prefix)}(\\d{{4}})\\.[^.]+$"
        match = re.match(pattern, filename)
        if not match:
            return None
        return int(match.group(1))
