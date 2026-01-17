import os
from .base_run_config import BaseRunConfig
from backend.album_storage.folder_album_handler import FolderAlbumHandler


class TryCameraModule(BaseRunConfig):
    """Script for testing a camera module for debugging purposes.

    The script will create a folder named `test_albums` in the root
    directory of the project which will contain the image files
    created.

    """

    def __init__(self, *args, album_dir_name="test_albums", **kwargs):
        super().__init__(*args, **kwargs)
        self.album_dir_name = album_dir_name

    def run(self):
        self.__ensure_album_directory_exists()
        album_handler = FolderAlbumHandler(".", self.album_dir_name)

        camera_module_name = self.args.camera_module
        album_name = camera_module_name + "_album"
        album = album_handler.get_or_create_album(album_name)

        print("Capturing image with {} module to {}/{}".format(
            camera_module_name,
            self.album_dir_name,
            album_name
        ))
        camera_module = self.get_camera_module_instance()
        album.try_capture_image_to_album(camera_module)

    def __ensure_album_directory_exists(self):
        if not os.path.exists(self.album_dir_name):
            os.makedirs(self.album_dir_name)
