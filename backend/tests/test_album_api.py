import unittest
import tempfile
import os
import json
from backend.app import create_app
from backend.album_storage.folder_album_handler import FolderAlbumHandler
from backend.qr_code_api.qr_code_handler import QrCodeHandler
from .camera_modules_for_testing import create_fast_dummy_module, FaultyCameraModule
from .test_utils import temp_dir_relpath


class AlbumApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # Creates a temporary static dir which is deleted after every test
        self.static_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_dir_name = temp_dir_relpath(self.static_dir)
        self.album_dir_path = os.path.join(self.static_dir_name, "albums")

        self.camera_module = create_fast_dummy_module()
        self.create_app_and_client_with_camera_module(self.camera_module)

    def create_app_and_client_with_camera_module(self, camera_module) -> None:
        self.album_handler = FolderAlbumHandler(self.static_dir_name, "albums")
        qr_code_handler = QrCodeHandler(self.static_dir_name)
        app = create_app(self.album_handler, self.static_dir_name, camera_module, qr_code_handler)
        self.test_client = app.test_client()

    def create_app_and_client_with_forced_album(self, forced_album_name) -> None:
        self.album_handler = FolderAlbumHandler(self.static_dir_name, "albums")
        qr_code_handler = QrCodeHandler(self.static_dir_name)
        app = create_app(
            self.album_handler,
            self.static_dir_name,
            self.camera_module,
            qr_code_handler,
            forced_album_name=forced_album_name
        )
        self.test_client = app.test_client()

    def tearDown(self) -> None:
        self.static_dir.cleanup()

    def create_temp_album(self, album_name, description="") -> None:
        """Create an album with the specified name and description."""
        self.album_handler.get_or_create_album(album_name, description)

    def add_dummy_image_file_to_album(self, album_name) -> None:
        album = self.album_handler.get_album(album_name)
        album.try_capture_image_to_album(self.camera_module)

    def test_no_available_albums_when_there_are_none(self) -> None:
        response = self.test_client.get('/albums/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'available_albums': []})

    def test_get_available_albums_after_creating_two_albums(self) -> None:
        self.create_temp_album("album2")
        self.create_temp_album("album1")

        response = self.test_client.get('/albums/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {'available_albums': ['album1', 'album2']}
        self.assertEqual(response.json, expected_response)

    def test_get_available_albums_when_forced_album_is_set(self) -> None:
        self.create_temp_album("album2")
        self.create_temp_album("album1")

        self.create_app_and_client_with_forced_album("album2")

        json_response = self.test_client.get('/albums/', content_type='application/json').json

        expected_response = {"forced_album": "album2"}
        self.assertEqual(json_response, expected_response)

    def test_create_album_when_forced_album_is_set(self) -> None:
        self.create_temp_album("album2")

        self.create_app_and_client_with_forced_album("album2")

        PARAMS = {
            "album_name": "album1",
            "description": "A very nice album indeed"
        }
        json_response = self.test_client.post(
            '/albums/',
            data=json.dumps(PARAMS),
            content_type='application/json',
            follow_redirects=True
        ).json

        expected_response = {'error': 'Illegal operation. The only accessible album is album2.'}
        self.assertEqual(json_response, expected_response)

    def test_response_from_creating_album(self) -> None:
        PARAMS = {
            "album_name": "album1",
            "description": "A very nice album indeed"
        }
        # This request should create the album specified with PARAMS
        json_response = self.test_client.post(
            '/albums/',
            data=json.dumps(PARAMS),
            content_type='application/json',
            follow_redirects=True
        ).json

        expected_response = {
            'album_name': 'album1',
            'album_url': '/albums/album1'
        }
        self.assertEqual(json_response, expected_response)

    def test_album_exists_after_create_album_request(self) -> None:
        PARAMS = {
            "album_name": "album1",
            "description": "A very nice album indeed"
        }
        self.test_client.post(
            '/albums/',
            data=json.dumps(PARAMS),
            content_type='application/json',
            follow_redirects=True
        )

        self.assertTrue(self.album_handler.album_exists("album1"))
        album = self.album_handler.get_album("album1")
        self.assertEqual(album.get_album_description(), "A very nice album indeed")

    def test_create_album_without_album_name_parameter_gives_error(self) -> None:
        # This request should give an error as we have no album_name parameter
        json_response = self.test_client.post('/albums/', content_type='application/json').json
        self.assertEqual(json_response, {'error': 'Missing required parameter <album_name>'})

    def test_update_album_description(self) -> None:
        self.create_temp_album("album1", description="This is not a very nice album")
        PARAMS = {
            "album_name": "album1",
            "description": "This is definitely a very nice album"
        }
        # This request should update the album description
        json_response = self.test_client.post(
            '/albums/',
            data=json.dumps(PARAMS),
            content_type='application/json',
            follow_redirects=True).json

        self.assertEqual(json_response, {'album_name': 'album1', 'album_url': '/albums/album1'})
        self.assertEqual(self.album_handler.get_available_album_names(), ["album1"])
        album1 = self.album_handler.get_album("album1")
        self.assertEqual(album1.get_album_description(), "This is definitely a very nice album")

    def test_get_info_for_nonexistent_album(self) -> None:
        # This request should give an error as album1 does not exist
        json_response = self.test_client.get('/albums/album1', content_type='application/json').json
        self.assertEqual(json_response, {
            "error": "No album with the name \"album1\" exists"
        })

    def test_get_info_for_forced_album(self) -> None:
        self.create_temp_album("album1")
        self.create_app_and_client_with_forced_album("album1")
        json_response = self.test_client.get('/albums/album1', content_type='application/json').json
        self.assertEqual(json_response, {
            'album_name': 'album1',
            'description': '',
            'image_urls': [],
            'thumbnail_urls': []
        })

    def test_get_info_for_album_other_than_forced_album(self) -> None:
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        self.create_app_and_client_with_forced_album("album2")
        json_response = self.test_client.get('/albums/album1', content_type='application/json').json
        self.assertEqual(json_response, {"error": "Illegal operation. The only accessible album is album2."})

    def test_get_info_for_album_without_description(self) -> None:
        self.create_temp_album("album1")
        json_response = self.test_client.get('/albums/album1', content_type='application/json').json
        self.assertEqual(json_response, {
            'album_name': 'album1',
            'description': '',
            'image_urls': [],
            'thumbnail_urls': []
        })

    def test_get_info_for_album_with_description(self) -> None:
        self.create_temp_album("album1", description="This is a very nice album")
        json_response = self.test_client.get('/albums/album1', content_type='application/json').json
        self.assertEqual(json_response, {
            'album_name': 'album1',
            'description': 'This is a very nice album',
            'image_urls': [],
            'thumbnail_urls': []
        })

    def test_get_info_for_album_with_images(self) -> None:
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")

        json_response = self.test_client.get('/albums/album1', content_type='application/json').json
        self.assertEqual(json_response, {
            'album_name': 'album1',
            'description': '',
            'image_urls': [
                '/{}/albums/album1/images/image0002.png'.format(self.static_dir_name),
                '/{}/albums/album1/images/image0001.png'.format(self.static_dir_name)
            ],
            'thumbnail_urls': [
                '/{}/albums/album1/thumbnails/image0002.jpg'.format(self.static_dir_name),
                '/{}/albums/album1/thumbnails/image0001.jpg'.format(self.static_dir_name)
            ]
        })

    def test_capture_image_to_album_which_is_not_forced(self) -> None:
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        self.create_app_and_client_with_forced_album("album2")

        json_response = self.test_client.post(
            "/albums/album1",
            content_type='application/json',
            follow_redirects=True
        ).json
        self.assertEqual(json_response, {"error": "Illegal operation. The only accessible album is album2."})

    def test_successful_image_capture_response(self) -> None:
        self.create_temp_album("album1")
        json_response = self.test_client.post(
            "/albums/album1",
            content_type='application/json',
            follow_redirects=True
        ).json
        self.assertEqual(json_response, {
            'image_url': "/{}/albums/album1/images/image0001.png".format(self.static_dir_name),
            'success': 'Image successfully captured',
            'thumbnail_url': "/{}/albums/album1/thumbnails/image0001.jpg".format(self.static_dir_name)
        })

    def test_unsuccessful_image_capture_response(self) -> None:
        self.create_app_and_client_with_camera_module(FaultyCameraModule())
        self.create_temp_album("album1")
        json_response = self.test_client.post(
            "/albums/album1",
            content_type='application/json',
            follow_redirects=True
        ).json
        self.assertEqual(json_response, {'error': 'This is a test error message'})

    def test_camera_is_not_busy_after_failed_capture(self) -> None:
        faulty_module = FaultyCameraModule()
        self.create_app_and_client_with_camera_module(faulty_module)
        self.create_temp_album("album1")

        self.test_client.post(
            "/albums/album1",
            content_type='application/json',
            follow_redirects=True
        ).json  # This request should fail
        faulty_module.should_fail = False

        json_response = self.test_client.post(
            "/albums/album1",
            content_type='application/json',
            follow_redirects=True
        ).json
        self.assertNotIn("error", json_response)

    def test_get_last_image_for_album_on_empty_album(self) -> None:
        self.create_temp_album("album1")
        json_response = self.test_client.get("/albums/album1/last_image").json
        self.assertEqual(json_response, {'error': 'album is empty'})

    def test_get_last_image_for_not_forced_album(self) -> None:
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        self.create_app_and_client_with_forced_album("album2")

        json_response = self.test_client.get("/albums/album1/last_image").json
        self.assertEqual(json_response, {"error": "Illegal operation. The only accessible album is album2."})

    def test_get_last_image_for_album_after_adding_image(self) -> None:
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")

        json_response = self.test_client.get("/albums/album1/last_image").json
        self.assertEqual(json_response, {
            'last_image_url': "/{}/albums/album1/images/image0001.png".format(self.static_dir_name)

        })

    def test_get_last_image_for_album_after_adding_two_images(self) -> None:
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")

        json_response = self.test_client.get("/albums/album1/last_image").json
        self.assertEqual(json_response, {
            'last_image_url': "/{}/albums/album1/images/image0002.png".format(self.static_dir_name)
        })


if __name__ == '__main__':
    unittest.main()
