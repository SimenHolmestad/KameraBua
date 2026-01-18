import os
from backend.album_storage.folder_album_handler import FolderAlbumHandler
from backend.config_loader import load_settings
from backend.settings import Settings
from scripts.shared.utils import get_camera_module_instance


def run_try_camera_module(settings: Settings, album_dir_name: str = "test_albums") -> None:
    """Script for testing a camera module for debugging purposes.

    The script will create a folder named `test_albums` in the root
    directory of the project which will contain the image files
    created.

    """
    ensure_album_directory_exists(album_dir_name)
    album_handler = FolderAlbumHandler(".", album_dir_name)

    camera_module_name = settings.camera.module
    album_name = camera_module_name + "_album"
    album = album_handler.get_or_create_album(album_name)

    print("Capturing image with {} module to {}/{}".format(
        camera_module_name,
        album_dir_name,
        album_name
    ))
    camera_module = get_camera_module_instance(settings)
    album.try_capture_image_to_album(camera_module)


def ensure_album_directory_exists(album_dir_name: str) -> None:
    if not os.path.exists(album_dir_name):
        os.makedirs(album_dir_name)


def main() -> None:
    settings = load_settings()
    run_try_camera_module(settings)


if __name__ == "__main__":
    main()
