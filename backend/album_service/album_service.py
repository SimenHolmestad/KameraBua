import os
from types import SimpleNamespace
from typing import List, Optional, Tuple
from .current_image_tracker import (
    get_name_of_last_image,
    get_next_image_name,
    increase_image_number
)
from .image_name_formatter import change_extension_of_filename
from .thumbnail_utils import create_thumbnail_for_image, recreate_all_thumbnails
from backend.camera_service import camera_service
from backend.core.config import AlbumConfig, CameraConfig

DEFAULT_IMAGE_NAME_PREFIX = "image"


class AlbumNotFoundError(RuntimeError):
    pass


class AlbumService:
    def __init__(self, config: AlbumConfig, camera_config: CameraConfig) -> None:
        self.config = config
        self.camera_config = camera_config
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
        image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX
    ) -> Optional[str]:
        self._ensure_album_folders(album_name)
        return get_name_of_last_image(
            self._album_path(album_name),
            self._images_path(album_name),
            image_name_prefix
        )

    def get_last_thumbnail_name(
        self,
        album_name: str,
        image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX
    ) -> Optional[str]:
        last_image_name = self.get_last_image_name(album_name, image_name_prefix)
        if not last_image_name:
            return None
        return change_extension_of_filename(last_image_name, ".jpg")

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
        image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX
    ) -> Tuple[str, str]:
        self._ensure_album_folders(album_name)
        album_path = self._album_path(album_name)
        images_path = self._images_path(album_name)
        thumbnails_path = self._thumbnails_path(album_name)

        module_name = self.camera_config.module
        module_config = self.camera_config.modules.get(module_name)
        if not module_config:
            raise camera_service.CameraModuleNotFoundError(
                f"Unknown camera module: {module_name}"
            )
        file_extension = module_config.get("file_extension")
        if not file_extension:
            raise camera_service.ImageCaptureError(
                f"Missing file extension for camera module: {module_name}"
            )

        next_image_name = get_next_image_name(
            album_path,
            images_path,
            image_name_prefix,
            file_extension
        )

        if module_config.get("needs_raw_file_transfer"):
            raw_images_path = self._raw_images_path(album_name)
            os.makedirs(raw_images_path, exist_ok=True)
            raw_extension = module_config.get("raw_file_extension")
            if not raw_extension:
                raise camera_service.ImageCaptureError(
                    f"Missing raw file extension for camera module: {module_name}"
                )
            raw_image_name = change_extension_of_filename(next_image_name, raw_extension)
            raw_image_path = os.path.join(raw_images_path, raw_image_name)
            image_path = os.path.join(images_path, next_image_name)
            camera_service.try_capture_image(
                SimpleNamespace(camera=self.camera_config),
                image_path,
                raw_image_path
            )
        else:
            image_path = os.path.join(images_path, next_image_name)
            camera_service.try_capture_image(SimpleNamespace(camera=self.camera_config), image_path)

        create_thumbnail_for_image(images_path, thumbnails_path, next_image_name)
        increase_image_number(album_path, images_path, image_name_prefix)

        thumbnail_name = change_extension_of_filename(next_image_name, ".jpg")
        return next_image_name, thumbnail_name

    def ensure_album_thumbnails_correct(self, album_name: str) -> None:
        self._ensure_album_folders(album_name)
        thumbnails_path = self._thumbnails_path(album_name)
        images_path = self._images_path(album_name)
        os.makedirs(thumbnails_path, exist_ok=True)
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

    def _raw_images_path(self, album_name: str) -> str:
        return os.path.join(self._album_path(album_name), "raw_images")

    def _ensure_album_folders(self, album_name: str) -> None:
        os.makedirs(self.config.albums_dir, exist_ok=True)
        os.makedirs(self._album_path(album_name), exist_ok=True)
        os.makedirs(self._images_path(album_name), exist_ok=True)
        os.makedirs(self._thumbnails_path(album_name), exist_ok=True)
