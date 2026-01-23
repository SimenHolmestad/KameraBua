import argparse
import os
from backend.album_service import album_service
from backend.core.config_loader import load_config
from backend.core.config import Config


def run_try_camera_module(config: Config, album_dir_name: str = "test_albums") -> None:
    """Script for testing a camera module for debugging purposes.

    The script will create a folder named `test_albums` in the root
    directory of the project which will contain the image files
    created.

    """
    ensure_album_directory_exists(album_dir_name)
    base_path = "."

    camera_module_name = config.camera.module
    album_name = camera_module_name + "_album"
    album_service.get_or_create_album(base_path, album_dir_name, album_name)

    print(f"Capturing image with {camera_module_name} module to {album_dir_name}/{album_name}")
    album_service.capture_image_to_album(base_path, album_dir_name, album_name, config)


def ensure_album_directory_exists(album_dir_name: str) -> None:
    if not os.path.exists(album_dir_name):
        os.makedirs(album_dir_name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Try camera module capture.")
    parser.add_argument(
        "config",
        nargs="?",
        default=os.path.join("configs", "example_config.json"),
        help="Path to a config file."
    )
    args = parser.parse_args()
    config = load_config(args.config)
    run_try_camera_module(config)


if __name__ == "__main__":
    main()
