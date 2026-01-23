import os
import shutil
import unittest
import tempfile
from backend.album_service import album_service
from .camera_modules_for_testing import create_fast_dummy_config, create_dummy_raw_config
from .test_utils import temp_dir_relpath


class FolderAlbumTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory(dir=".")
        self.test_dir_name = temp_dir_relpath(self.test_dir)
        self.base_path = "."
        self.albums_dir = self.test_dir_name
        self.album_name = "test_album"
        album_service.get_or_create_album(self.base_path, self.albums_dir, self.album_name)

    def tearDown(self) -> None:
        self.test_dir.cleanup()  # Remove test_dir from file system

    def add_dummy_image_file_to_album(self, album_name, image_name) -> None:
        """Create a dummy image file with the specified name to the specified album."""
        path_to_image_file = os.path.join(
            self.test_dir_name,
            album_name,
            "images",
            image_name
        )
        open(path_to_image_file, 'a').close()

    def create_current_image_number_file(self, album_name, current_image_number) -> None:
        current_image_number_file_path = os.path.join(
            self.test_dir_name,
            album_name,
            ".image_number.txt"
        )

        with open(current_image_number_file_path, "w") as file_handle:
            file_handle.write(str(current_image_number))

    def test_creating_album_creates_album_folder(self) -> None:
        expected_album_folder_path = os.path.join(
            self.test_dir_name,
            self.album_name
        )
        self.assertTrue(os.path.exists(expected_album_folder_path))

    def test_creating_album_creates_images_folder(self) -> None:
        expected_images_folder_path = os.path.join(
            self.test_dir_name,
            self.album_name,
            "images"
        )
        self.assertTrue(os.path.exists(expected_images_folder_path))

    def test_creating_album_creates_thumbnails_folder(self) -> None:
        expected_thumbnails_folder_path = os.path.join(
            self.test_dir_name,
            self.album_name,
            "thumbnails"
        )
        self.assertTrue(os.path.exists(expected_thumbnails_folder_path))

    def test_newly_created_album_has_no_description(self) -> None:
        description = album_service.get_album_description(
            self.base_path,
            self.albums_dir,
            self.album_name
        )
        self.assertEqual(description, "")

    def test_newly_created_album_has_no_last_image(self) -> None:
        last_image = album_service.get_relative_url_of_last_image(
            self.base_path,
            self.albums_dir,
            self.album_name
        )
        self.assertEqual(last_image, None)

    def test_newly_created_album_has_no_last_thumbnail(self) -> None:
        last_thumbnail = album_service.get_relative_url_of_last_thumbnail(
            self.base_path,
            self.albums_dir,
            self.album_name
        )
        self.assertEqual(last_thumbnail, None)

    def test_set_album_description(self) -> None:
        album_service.set_album_description(
            self.base_path,
            self.albums_dir,
            self.album_name,
            "This album is a test"
        )
        description = album_service.get_album_description(
            self.base_path,
            self.albums_dir,
            self.album_name
        )
        self.assertEqual(description, "This album is a test")

    def test_capture_image_to_album(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_relative_image_url = f"{self.test_dir_name}/test_album/images/image0001.png"
        expected_relative_thumbnail_url = f"{self.test_dir_name}/test_album/thumbnails/image0001.jpg"

        last_image_url = album_service.get_relative_url_of_last_image(
            self.base_path,
            self.albums_dir,
            self.album_name
        )
        last_thumbnail_url = album_service.get_relative_url_of_last_thumbnail(
            self.base_path,
            self.albums_dir,
            self.album_name
        )

        self.assertEqual(last_image_url, expected_relative_image_url)
        self.assertEqual(last_thumbnail_url, expected_relative_thumbnail_url)

    def test_captured_image_exists(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0001.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_after_externally_adding_files(self) -> None:
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")

        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0004.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_after_externally_adding_files_weird_order(self) -> None:
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0017.jpg")

        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0018.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_with_wrong_image_number_file(self) -> None:
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")
        self.create_current_image_number_file("test_album", 20)

        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0004.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_creates_thumbnail(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_thumbnail_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails",
            "image0001.jpg"
        )

        self.assertTrue(os.path.exists(expected_thumbnail_filepath))

    def test_image_and_thumbnail_same_number_after_capture(self) -> None:
        config = create_fast_dummy_config()
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")

        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        expected_thumbnail_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails",
            "image0004.jpg"
        )

        self.assertTrue(os.path.exists(expected_thumbnail_filepath))

    def test_capture_image_with_camera_module_requiring_raw_image_transfer(self) -> None:
        raw_config = create_dummy_raw_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            raw_config
        )

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0001.png"
        )
        self.assertTrue(os.path.exists(expected_image_filepath))

        expected_raw_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "raw_images",
            "image0001.cr2"
        )
        self.assertTrue(os.path.exists(expected_raw_image_filepath))

    def test_ensure_thumbnails_correct(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        thumbnails_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        shutil.rmtree(thumbnails_path)  # Remove thumbnails folder

        album_service.ensure_album_thumbnails_correct(self.base_path, self.albums_dir, self.album_name)

        thumbnails_folder_content = os.listdir(thumbnails_path)
        self.assertEqual(thumbnails_folder_content, ['image0001.jpg', 'image0002.jpg'])

    def test_ensure_thumbnails_correct_with_deleted_image(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        path_to_image2 = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0002.png"
        )
        os.remove(path_to_image2)
        album_service.ensure_album_thumbnails_correct(self.base_path, self.albums_dir, self.album_name)

        thumbnails_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        thumbnails_folder_content = os.listdir(thumbnails_path)
        self.assertEqual(thumbnails_folder_content, ['image0001.jpg', 'image0003.jpg'])

    def test_get_url_of_all_images(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        relative_image_urls = album_service.get_relative_urls_of_all_images(
            self.base_path,
            self.albums_dir,
            self.album_name
        )

        expected_realtive_image_urls = [
            self.test_dir_name + "/test_album/images/image0003.png",
            self.test_dir_name + "/test_album/images/image0002.png",
            self.test_dir_name + "/test_album/images/image0001.png",
        ]
        self.assertEqual(relative_image_urls, expected_realtive_image_urls)

    def test_get_url_of_all_thumbnails(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        relative_thumbnail_urls = album_service.get_relative_urls_of_all_thumbnails(
            self.base_path,
            self.albums_dir,
            self.album_name
        )

        expected_relative_thumnail_urls = [
            self.test_dir_name + "/test_album/thumbnails/image0002.jpg",
            self.test_dir_name + "/test_album/thumbnails/image0001.jpg",
        ]
        self.assertEqual(relative_thumbnail_urls, expected_relative_thumnail_urls)

    def test_album_empty_after_deleting_all_images(self) -> None:
        config = create_fast_dummy_config()
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )
        album_service.capture_image_to_album(
            self.base_path,
            self.albums_dir,
            self.album_name,
            config
        )

        images_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "images"
        )
        shutil.rmtree(images_path)  # Remove images folder
        os.mkdir(images_path)

        last_image = album_service.get_relative_url_of_last_image(
            self.base_path,
            self.albums_dir,
            self.album_name
        )
        self.assertEqual(last_image, None)


if __name__ == '__main__':
    unittest.main()
