import os
import shutil
from typing import List, Optional, Tuple
from PIL import Image
from .current_image_tracker import (
    get_name_of_last_image,
    get_next_image_name,
    increase_image_number
)
from .image_name_formatter import change_extension_of_filename
from backend.camera_service import camera_service
from backend.core.config import Config

MAX_THUMBNAIL_SIZE = (600, 600)
DEFAULT_ALBUMS_DIR = "albums"
DEFAULT_IMAGE_NAME_PREFIX = "image"


class AlbumNotFoundError(RuntimeError):
    pass


def get_available_album_names(base_path: str, albums_dir: str = DEFAULT_ALBUMS_DIR) -> List[str]:
    albums_root = _albums_root_path(base_path, albums_dir)
    os.makedirs(albums_root, exist_ok=True)
    return sorted(os.listdir(albums_root))


def album_exists(base_path: str, albums_dir: str, album_name: str) -> bool:
    return os.path.exists(_album_path(base_path, albums_dir, album_name))


def get_album_path_or_error(base_path: str, albums_dir: str, album_name: str) -> str:
    album_path = _album_path(base_path, albums_dir, album_name)
    if not os.path.exists(album_path):
        raise AlbumNotFoundError()
    return album_path


def get_or_create_album(
    base_path: str,
    albums_dir: str,
    album_name: str,
    description: str = ""
) -> None:
    _ensure_album_folders(base_path, albums_dir, album_name)
    if description:
        set_album_description(base_path, albums_dir, album_name, description)


def get_album_description(base_path: str, albums_dir: str, album_name: str) -> str:
    description_path = os.path.join(_album_path(base_path, albums_dir, album_name), "description.txt")
    if not os.path.exists(description_path):
        return ""
    with open(description_path, "r") as file_handle:
        return file_handle.read()


def set_album_description(base_path: str, albums_dir: str, album_name: str, content: str) -> None:
    _ensure_album_folders(base_path, albums_dir, album_name)
    description_path = os.path.join(_album_path(base_path, albums_dir, album_name), "description.txt")
    with open(description_path, "w") as file_handle:
        file_handle.write(content)


def get_relative_url_of_last_image(
    base_path: str,
    albums_dir: str,
    album_name: str,
    image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX
) -> Optional[str]:
    _ensure_album_folders(base_path, albums_dir, album_name)
    last_image_name = get_name_of_last_image(
        _album_path(base_path, albums_dir, album_name),
        _images_path(base_path, albums_dir, album_name),
        image_name_prefix
    )
    if not last_image_name:
        return None
    return _relative_url(albums_dir, album_name, "images", last_image_name)


def get_relative_url_of_last_thumbnail(
    base_path: str,
    albums_dir: str,
    album_name: str,
    image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX
) -> Optional[str]:
    _ensure_album_folders(base_path, albums_dir, album_name)
    last_image_name = get_name_of_last_image(
        _album_path(base_path, albums_dir, album_name),
        _images_path(base_path, albums_dir, album_name),
        image_name_prefix
    )
    if not last_image_name:
        return None
    thumbnail_name = change_extension_of_filename(last_image_name, ".jpg")
    return _relative_url(albums_dir, album_name, "thumbnails", thumbnail_name)


def get_relative_urls_of_all_images(
    base_path: str,
    albums_dir: str,
    album_name: str
) -> List[str]:
    _ensure_album_folders(base_path, albums_dir, album_name)
    image_names = sorted(
        os.listdir(_images_path(base_path, albums_dir, album_name)),
        reverse=True
    )
    return [
        _relative_url(albums_dir, album_name, "images", name)
        for name in image_names
    ]


def get_relative_urls_of_all_thumbnails(
    base_path: str,
    albums_dir: str,
    album_name: str
) -> List[str]:
    _ensure_album_folders(base_path, albums_dir, album_name)
    thumbnail_names = sorted(
        os.listdir(_thumbnails_path(base_path, albums_dir, album_name)),
        reverse=True
    )
    return [
        _relative_url(albums_dir, album_name, "thumbnails", name)
        for name in thumbnail_names
    ]


def capture_image_to_album(
    base_path: str,
    albums_dir: str,
    album_name: str,
    config: Config,
    image_name_prefix: str = DEFAULT_IMAGE_NAME_PREFIX
) -> Tuple[str, str]:
    _ensure_album_folders(base_path, albums_dir, album_name)
    album_path = _album_path(base_path, albums_dir, album_name)
    images_path = _images_path(base_path, albums_dir, album_name)
    thumbnails_path = _thumbnails_path(base_path, albums_dir, album_name)

    module_name = config.camera.module
    module_config = config.camera.modules.get(module_name)
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
        raw_images_path = _raw_images_path(base_path, albums_dir, album_name)
        os.makedirs(raw_images_path, exist_ok=True)
        raw_extension = module_config.get("raw_file_extension")
        if not raw_extension:
            raise camera_service.ImageCaptureError(
                f"Missing raw file extension for camera module: {module_name}"
            )
        raw_image_name = change_extension_of_filename(next_image_name, raw_extension)
        raw_image_path = os.path.join(raw_images_path, raw_image_name)
        image_path = os.path.join(images_path, next_image_name)
        camera_service.try_capture_image(config, image_path, raw_image_path)
    else:
        image_path = os.path.join(images_path, next_image_name)
        camera_service.try_capture_image(config, image_path)

    _create_thumbnail_for_image(images_path, thumbnails_path, next_image_name)
    increase_image_number(album_path, images_path, image_name_prefix)

    image_url = _relative_url(albums_dir, album_name, "images", next_image_name)
    thumbnail_name = change_extension_of_filename(next_image_name, ".jpg")
    thumbnail_url = _relative_url(albums_dir, album_name, "thumbnails", thumbnail_name)
    return image_url, thumbnail_url


def ensure_album_thumbnails_correct(base_path: str, albums_dir: str, album_name: str) -> None:
    _ensure_album_folders(base_path, albums_dir, album_name)
    thumbnails_path = _thumbnails_path(base_path, albums_dir, album_name)
    images_path = _images_path(base_path, albums_dir, album_name)
    os.makedirs(thumbnails_path, exist_ok=True)
    if len(os.listdir(images_path)) != len(os.listdir(thumbnails_path)):
        _recreate_all_thumbnails(images_path, thumbnails_path)


def ensure_all_thumbnails_correct(base_path: str, albums_dir: str) -> None:
    for album_name in get_available_album_names(base_path, albums_dir):
        ensure_album_thumbnails_correct(base_path, albums_dir, album_name)


def _albums_root_path(base_path: str, albums_dir: str) -> str:
    return os.path.join(base_path, albums_dir)


def _album_path(base_path: str, albums_dir: str, album_name: str) -> str:
    return os.path.join(_albums_root_path(base_path, albums_dir), album_name)


def _images_path(base_path: str, albums_dir: str, album_name: str) -> str:
    return os.path.join(_album_path(base_path, albums_dir, album_name), "images")


def _thumbnails_path(base_path: str, albums_dir: str, album_name: str) -> str:
    return os.path.join(_album_path(base_path, albums_dir, album_name), "thumbnails")


def _raw_images_path(base_path: str, albums_dir: str, album_name: str) -> str:
    return os.path.join(_album_path(base_path, albums_dir, album_name), "raw_images")


def _ensure_album_folders(base_path: str, albums_dir: str, album_name: str) -> None:
    os.makedirs(_albums_root_path(base_path, albums_dir), exist_ok=True)
    os.makedirs(_album_path(base_path, albums_dir, album_name), exist_ok=True)
    os.makedirs(_images_path(base_path, albums_dir, album_name), exist_ok=True)
    os.makedirs(_thumbnails_path(base_path, albums_dir, album_name), exist_ok=True)


def _relative_url(albums_dir: str, album_name: str, folder_name: str, filename: str) -> str:
    return f"{albums_dir}/{album_name}/{folder_name}/{filename}"


def _create_thumbnail(input_path: str, output_path: str) -> None:
    image = Image.open(input_path)
    image = image.convert("RGB")
    image.thumbnail(MAX_THUMBNAIL_SIZE)
    image.save(output_path)


def _create_thumbnail_for_image(
    images_path: str,
    thumbnails_path: str,
    image_name: str
) -> None:
    thumbnail_name = change_extension_of_filename(image_name, ".jpg")
    thumbnail_path = os.path.join(thumbnails_path, thumbnail_name)
    image_path = os.path.join(images_path, image_name)
    _create_thumbnail(image_path, thumbnail_path)


def _recreate_all_thumbnails(images_path: str, thumbnails_path: str) -> None:
    shutil.rmtree(thumbnails_path)
    os.mkdir(thumbnails_path)
    image_names = sorted(os.listdir(images_path))
    for name in image_names:
        _create_thumbnail_for_image(images_path, thumbnails_path, name)
