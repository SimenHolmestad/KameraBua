import os
from typing import List, Optional
from .current_image_tracker import CurrentImageTracker
from .image_name_formatter import change_extension_of_filename
from .thumbnail_utils import create_thumbnail_for_image, recreate_all_thumbnails
from backend.camera_service import CameraService
from backend.core.config import AlbumConfig


class AlbumNotFoundError(RuntimeError):
    pass


class AlbumService:
    def __init__(self, config: AlbumConfig, camera_service: CameraService) -> None:
        self.config = config
        self.camera_service = camera_service
        os.makedirs(self.config.albums_dir, exist_ok=True)

    def get_available_album_names(self) -> List[str]:
        os.makedirs(self.config.albums_dir, exist_ok=True)
        return sorted(os.listdir(self.config.albums_dir))

    def album_exists(self, album_name: str) -> bool:
        return os.path.exists(self._album_path(album_name))

    def get_album_path_or_error(self, album_name: str) -> str:
        album_path = self._album_path(album_name)
        if not os.path.exists(album_path):
            raise AlbumNotFoundError()
        return album_path

    def get_or_create_album(self, album_name: str, description: str = "") -> None:
        self._ensure_album_folders(album_name)
        if description:
            self.set_album_description(album_name, description)

    def get_album_description(self, album_name: str) -> str:
        description_path = os.path.join(self._album_path(album_name), "description.txt")
        if not os.path.exists(description_path):
            return ""
        with open(description_path, "r") as file_handle:
            return file_handle.read()

    def set_album_description(self, album_name: str, content: str) -> None:
        self._ensure_album_folders(album_name)
        description_path = os.path.join(self._album_path(album_name), "description.txt")
        with open(description_path, "w") as file_handle:
            file_handle.write(content)

    def get_last_image_name(
        self,
        album_name: str,
    ) -> Optional[str]:
        self._ensure_album_folders(album_name)
        image_tracker = self._image_tracker_for_album(album_name)
        return image_tracker.get_name_of_last_image()

    def get_last_thumbnail_name(
        self,
        album_name: str,
    ) -> Optional[str]:
        last_image_name = self.get_last_image_name(album_name)
        if not last_image_name:
            return None
        return self._thumbnail_name_for_image(last_image_name)

    def get_image_names(self, album_name: str) -> List[str]:
        self._ensure_album_folders(album_name)
        return sorted(
            os.listdir(self._images_path(album_name)),
            reverse=True
        )

    def get_thumbnail_names(self, album_name: str) -> List[str]:
        self._ensure_album_folders(album_name)
        return sorted(
            os.listdir(self._thumbnails_path(album_name)),
            reverse=True
        )

    def capture_image_to_album(
        self,
        album_name: str,
    ) -> None:
        self._ensure_album_folders(album_name)
        image_tracker = self._image_tracker_for_album(album_name)
        images_path = self._images_path(album_name)
        next_image_base_name = self._capture_next_image(images_path, image_tracker)

        thumbnails_path = self._thumbnails_path(album_name)
        self._create_thumbnail_for_captured_image(images_path, thumbnails_path, next_image_base_name)

        image_tracker.increase_image_number()

    def ensure_album_thumbnails_correct(self, album_name: str) -> None:
        self._ensure_album_folders(album_name)
        thumbnails_path = self._thumbnails_path(album_name)
        images_path = self._images_path(album_name)
        if len(os.listdir(images_path)) != len(os.listdir(thumbnails_path)):
            recreate_all_thumbnails(images_path, thumbnails_path)

    def ensure_all_thumbnails_correct(self) -> None:
        for album_name in self.get_available_album_names():
            self.ensure_album_thumbnails_correct(album_name)

    def _album_path(self, album_name: str) -> str:
        return os.path.join(self.config.albums_dir, album_name)

    def _images_path(self, album_name: str) -> str:
        return os.path.join(self._album_path(album_name), "images")

    def _thumbnails_path(self, album_name: str) -> str:
        return os.path.join(self._album_path(album_name), "thumbnails")

    def _ensure_album_folders(self, album_name: str) -> None:
        os.makedirs(self.config.albums_dir, exist_ok=True)
        os.makedirs(self._album_path(album_name), exist_ok=True)
        os.makedirs(self._images_path(album_name), exist_ok=True)
        os.makedirs(self._thumbnails_path(album_name), exist_ok=True)

    def _image_tracker_for_album(self, album_name: str) -> CurrentImageTracker:
        return CurrentImageTracker(
            album_folder_path=self._album_path(album_name),
            images_folder_path=self._images_path(album_name)
        )

    def _capture_next_image(
        self,
        images_path: str,
        image_tracker: CurrentImageTracker
    ) -> str:
        next_image_base_name = image_tracker.get_next_image_base_name()
        next_image_base_path = os.path.join(images_path, next_image_base_name)
        self.camera_service.capture_image(next_image_base_path)
        return next_image_base_name

    def _create_thumbnail_for_captured_image(
        self,
        images_path: str,
        thumbnails_path: str,
        image_base_name: str
    ) -> None:
        create_thumbnail_for_image(images_path, thumbnails_path, image_base_name)

    def _thumbnail_name_for_image(self, image_name: str) -> str:
        return change_extension_of_filename(image_name, ".jpg")
