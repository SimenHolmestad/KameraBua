import os
import shutil
import unittest
import tempfile
from backend.album_service import album_service
from backend.album_service.album_service import AlbumNotFoundError
from .camera_modules_for_testing import create_fast_dummy_config
from .test_utils import temp_dir_relpath


class FolderAlbumHandlerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory(dir=".")
        self.test_dir_name = temp_dir_relpath(self.test_dir)
        self.base_path = "./"
        self.albums_dir = self.test_dir_name

    def tearDown(self) -> None:
        self.test_dir.cleanup()  # Remove test_dir from file system

    def create_album_folder(self, name) -> None:
        path_to_folder = os.path.join(
            self.test_dir_name,
            name
        )
        os.mkdir(path_to_folder)

    def test_empty_folder_returns_empty_list(self) -> None:
        self.assertEqual(
            album_service.get_available_album_names(self.base_path, self.albums_dir),
            []
        )

    def test_accessing_nonexisting_album_causes_error(self) -> None:
        self.assertRaises(
            AlbumNotFoundError,
            album_service.get_album_path_or_error,
            self.base_path,
            self.albums_dir,
            "non-existing-album"
        )

    def test_access_existing_album_returns_album_class_object(self) -> None:
        self.create_album_folder("test_album")
        album_path = album_service.get_album_path_or_error(self.base_path, self.albums_dir, "test_album")
        self.assertTrue(os.path.exists(album_path))

    def test_create_new_album_without_description(self) -> None:
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album", "")
        description = album_service.get_album_description(self.base_path, self.albums_dir, "test_album")
        self.assertEqual(description, "")

    def test_album_names_in_available_album_names_after_creating_albums(self) -> None:
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album1", "")
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album2", "")
        self.assertEqual(
            album_service.get_available_album_names(self.base_path, self.albums_dir),
            ["test_album1", "test_album2"]
        )

    def test_create_new_album_with_description(self) -> None:
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album", "This is an album")
        description = album_service.get_album_description(self.base_path, self.albums_dir, "test_album")
        self.assertEqual(description, "This is an album")

    def test_nonexistent_album_does_not_exist(self) -> None:
        self.assertFalse(album_service.album_exists(self.base_path, self.albums_dir, "test_album"))

    def test_existing_album_does_exist(self) -> None:
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album", "This is an album")
        self.assertTrue(album_service.album_exists(self.base_path, self.albums_dir, "test_album"))

    def test_get_album_second_time(self) -> None:
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album", "This is an album")
        album_path = album_service.get_album_path_or_error(self.base_path, self.albums_dir, "test_album")
        self.assertTrue(os.path.exists(album_path))

    def test_ensure_all_thumbnails_correct(self) -> None:
        album_service.get_or_create_album(self.base_path, self.albums_dir, "test_album")
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(self.base_path, self.albums_dir, "test_album", config)
        album_service.capture_image_to_album(self.base_path, self.albums_dir, "test_album", config)

        thumbnails_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        shutil.rmtree(thumbnails_path)  # Remove thumbnails folder

        album_service.ensure_all_thumbnails_correct(self.base_path, self.albums_dir)
        thumbnails_folder_content = os.listdir(thumbnails_path)
        self.assertEqual(thumbnails_folder_content, ['image0001.jpg', 'image0002.jpg'])


if __name__ == '__main__':
    unittest.main()
