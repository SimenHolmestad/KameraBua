import os
import shutil
import unittest
import tempfile
from backend.album_storage.folder_album_handler import FolderAlbumHandler, AlbumNotFoundError
from backend.album_storage.base_album import BaseAlbum
from .camera_modules_for_testing import create_fast_dummy_module
from .test_utils import temp_dir_relpath


class FolderAlbumHandlerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory(dir=".")
        self.test_dir_name = temp_dir_relpath(self.test_dir)
        self.album_handler = FolderAlbumHandler("./", self.test_dir_name)

    def tearDown(self) -> None:
        self.test_dir.cleanup()  # Remove test_dir from file system

    def create_album_folder(self, name) -> None:
        path_to_folder = os.path.join(
            self.test_dir_name,
            name
        )
        os.mkdir(path_to_folder)

    def test_empty_folder_returns_empty_list(self) -> None:
        self.assertEqual(self.album_handler.get_available_album_names(), [])

    def test_accessing_nonexisting_album_causes_error(self) -> None:
        self.assertRaises(AlbumNotFoundError, self.album_handler.get_album, "non-existing-album")

    def test_access_existing_album_returns_album_class_object(self) -> None:
        self.create_album_folder("test_album")
        album = self.album_handler.get_album("test_album")
        self.assertTrue(isinstance(album, BaseAlbum))

    def test_create_new_album_without_description(self) -> None:
        album = self.album_handler.get_or_create_album("test_album", "")
        self.assertEqual(album.get_album_description(), "")

    def test_album_names_in_available_album_names_after_creating_albums(self) -> None:
        self.album_handler.get_or_create_album("test_album1", "")
        self.album_handler.get_or_create_album("test_album2", "")
        self.assertEqual(self.album_handler.get_available_album_names(), ["test_album1", "test_album2"])

    def test_create_new_album_with_description(self) -> None:
        album = self.album_handler.get_or_create_album("test_album", "This is an album")
        self.assertEqual(album.get_album_description(), "This is an album")

    def test_nonexistent_album_does_not_exist(self) -> None:
        self.assertFalse(self.album_handler.album_exists("test_album"))

    def test_existing_album_does_exist(self) -> None:
        self.album_handler.get_or_create_album("test_album", "This is an album")
        self.assertTrue(self.album_handler.album_exists("test_album"))

    def test_get_album_second_time(self) -> None:
        self.album_handler.get_or_create_album("test_album", "This is an album")
        album = self.album_handler.get_album("test_album")
        self.assertTrue(isinstance(album, BaseAlbum))

    def test_ensure_all_thumbnails_correct(self) -> None:
        album = self.album_handler.get_or_create_album("test_album")
        camera_module = create_fast_dummy_module()
        album.try_capture_image_to_album(camera_module)
        album.try_capture_image_to_album(camera_module)

        thumbnails_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        shutil.rmtree(thumbnails_path)  # Remove thumbnails folder

        self.album_handler.ensure_all_thumbnails_correct()
        thumbnails_folder_content = os.listdir(thumbnails_path)
        self.assertEqual(thumbnails_folder_content, ['image0001.jpg', 'image0002.jpg'])


if __name__ == '__main__':
    unittest.main()
