import argparse
import os
from backend.album_service.album_service import AlbumService
from backend.core.config_loader import load_config
from backend.core.config import Config


def run_try_camera_module(config: Config) -> None:
    """Script for testing a camera module for debugging purposes.

    The script will create a folder named `test_albums` in the root
    directory of the project which will contain the image files
    created.

    """
    camera_module_name = config.camera.module
    service = AlbumService(config.albums, config.camera)
    album_dir_name = config.albums.albums_dir
    album_name = camera_module_name + "_album"
    service.get_or_create_album(album_name)

    print(f"Capturing image with {camera_module_name} module to {album_dir_name}/{album_name}")
    service.capture_image_to_album(album_name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Try camera module capture.")
    parser.add_argument(
        "--env-file",
        dest="env_file",
        default=None,
        help="Path to a .env file."
    )
    args = parser.parse_args()
    env_file = args.env_file or os.path.join(".env")
    config = load_config(env_file)
    run_try_camera_module(config)


if __name__ == "__main__":
    main()
