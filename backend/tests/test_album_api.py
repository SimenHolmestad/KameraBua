import unittest
import tempfile
import os
from fastapi.testclient import TestClient
from backend.app import create_app
from backend.album_service.album_service import AlbumService
from scripts.shared import qr_code_utils
from .camera_modules_for_testing import create_fast_dummy_config, create_faulty_dummy_config
from .test_utils import temp_dir_relpath


class AlbumApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # Creates a temporary static dir which is deleted after every test
        self.static_dir = tempfile.TemporaryDirectory(dir="backend/static")
        self.static_dir_name = temp_dir_relpath(self.static_dir)
        self.albums_dir_path = os.path.join(self.static_dir_name, "albums")

        self.config = create_fast_dummy_config(self.albums_dir_path)
        self.create_app_and_client_with_config(self.config)

    def create_app_and_client_with_config(self, config) -> None:
        self.config = config
        self.album_service = AlbumService(config.albums, config.camera)
        qr_code_context = qr_code_utils.create_qr_code_context(self.static_dir_name)
        app = create_app(self.static_dir_name, config, qr_code_utils.get_qr_codes(qr_code_context))
        self.test_client = TestClient(app)

    def create_app_and_client_with_forced_album(self, forced_album_name) -> None:
        config = create_fast_dummy_config(self.albums_dir_path)
        config.albums.forced_album = forced_album_name
        self.config = config
        self.album_service = AlbumService(config.albums, config.camera)
        qr_code_context = qr_code_utils.create_qr_code_context(self.static_dir_name)
        app = create_app(self.static_dir_name, config, qr_code_utils.get_qr_codes(qr_code_context))
        self.test_client = TestClient(app)

    def tearDown(self) -> None:
        self.static_dir.cleanup()

    def create_temp_album(self, album_name, description="") -> None:
        """Create an album with the specified name and description."""
        self.album_service.get_or_create_album(album_name, description)

    def add_dummy_image_file_to_album(self, album_name) -> None:
        self.album_service.capture_image_to_album(album_name)

    def test_no_available_albums_when_there_are_none(self) -> None:
        response = self.test_client.get("/albums/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"available_albums": [], "forced_album": None})

    def test_get_available_albums_after_creating_two_albums(self) -> None:
        self.create_temp_album("album2")
        self.create_temp_album("album1")

        response = self.test_client.get("/albums/")
        self.assertEqual(response.status_code, 200)

        expected_response = {"available_albums": ["album1", "album2"]}
        self.assertEqual(response.json(), {**expected_response, "forced_album": None})

    def test_get_available_albums_when_forced_album_is_set(self) -> None:
        self.create_temp_album("album2")
        self.create_temp_album("album1")

        self.create_app_and_client_with_forced_album("album2")

        json_response = self.test_client.get("/albums/").json()

        expected_response = {"available_albums": ["album1", "album2"], "forced_album": "album2"}
        self.assertEqual(json_response, expected_response)

    def test_create_album_when_forced_album_is_set(self) -> None:
        self.create_temp_album("album2")

        self.create_app_and_client_with_forced_album("album2")

        PARAMS = {
            "album_name": "album1",
            "description": "A very nice album indeed"
        }
        response = self.test_client.post("/albums/", json=PARAMS)
        json_response = response.json()

        expected_response = {"error": "Illegal operation. The only accessible album is album2."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json_response, expected_response)

    def test_response_from_creating_album(self) -> None:
        PARAMS = {
            "album_name": "album1",
            "description": "A very nice album indeed"
        }
        # This request should create the album specified with PARAMS
        json_response = self.test_client.post("/albums/", json=PARAMS).json()

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
            "/albums/",
            json=PARAMS
        )

        self.assertTrue(self.album_service.album_exists("album1"))
        description = self.album_service.get_album_description("album1")
        self.assertEqual(description, "A very nice album indeed")

    def test_create_album_without_album_name_parameter_gives_error(self) -> None:
        # This request should give an error as we have no album_name parameter
        response = self.test_client.post("/albums/")
        self.assertEqual(response.status_code, 422)

    def test_update_album_description(self) -> None:
        self.create_temp_album("album1", description="This is not a very nice album")
        PARAMS = {
            "album_name": "album1",
            "description": "This is definitely a very nice album"
        }
        # This request should update the album description
        json_response = self.test_client.post("/albums/", json=PARAMS).json()

        self.assertEqual(json_response, {'album_name': 'album1', 'album_url': '/albums/album1'})
        self.assertEqual(
            self.album_service.get_available_album_names(),
            ["album1"]
        )
        description = self.album_service.get_album_description("album1")
        self.assertEqual(description, "This is definitely a very nice album")

    def test_get_info_for_nonexistent_album(self) -> None:
        # This request should give an error as album1 does not exist
        response = self.test_client.get("/albums/album1")
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, {
            "error": "No album with the name \"album1\" exists"
        })

    def test_get_info_for_forced_album(self) -> None:
        self.create_temp_album("album1")
        self.create_app_and_client_with_forced_album("album1")
        json_response = self.test_client.get("/albums/album1").json()
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
        response = self.test_client.get("/albums/album1")
        json_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json_response, {"error": "Illegal operation. The only accessible album is album2."})

    def test_get_info_for_album_without_description(self) -> None:
        self.create_temp_album("album1")
        json_response = self.test_client.get("/albums/album1").json()
        self.assertEqual(json_response, {
            'album_name': 'album1',
            'description': '',
            'image_urls': [],
            'thumbnail_urls': []
        })

    def test_get_info_for_album_with_description(self) -> None:
        self.create_temp_album("album1", description="This is a very nice album")
        json_response = self.test_client.get("/albums/album1").json()
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

        json_response = self.test_client.get("/albums/album1").json()
        self.assertEqual(json_response, {
            'album_name': 'album1',
            'description': '',
            'image_urls': [
                '/static/albums/album1/images/image0002.png',
                '/static/albums/album1/images/image0001.png'
            ],
            'thumbnail_urls': [
                '/static/albums/album1/thumbnails/image0002.jpg',
                '/static/albums/album1/thumbnails/image0001.jpg'
            ]
        })

    def test_capture_image_to_album_which_is_not_forced(self) -> None:
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        self.create_app_and_client_with_forced_album("album2")

        response = self.test_client.post("/albums/album1")
        json_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json_response, {"error": "Illegal operation. The only accessible album is album2."})

    def test_successful_image_capture_response(self) -> None:
        self.create_temp_album("album1")
        json_response = self.test_client.post("/albums/album1").json()
        self.assertEqual(json_response, {
            'image_url': "/static/albums/album1/images/image0001.png",
            'success': 'Image successfully captured',
            'thumbnail_url': "/static/albums/album1/thumbnails/image0001.jpg"
        })

    def test_unsuccessful_image_capture_response(self) -> None:
        faulty_config = create_faulty_dummy_config(self.albums_dir_path)
        self.create_app_and_client_with_config(faulty_config)
        self.create_temp_album("album1")
        response = self.test_client.post("/albums/album1")
        json_response = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json_response, {'error': 'This is a test error message'})

    def test_camera_is_not_busy_after_failed_capture(self) -> None:
        faulty_config = create_faulty_dummy_config(self.albums_dir_path)
        self.create_app_and_client_with_config(faulty_config)
        self.create_temp_album("album1")

        self.test_client.post(
            "/albums/album1"
        ).json()  # This request should fail
        faulty_config.camera.options["should_fail"] = False

        json_response = self.test_client.post("/albums/album1").json()
        self.assertNotIn("error", json_response)

    def test_get_last_image_for_album_on_empty_album(self) -> None:
        self.create_temp_album("album1")
        response = self.test_client.get("/albums/album1/last_image")
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, {'error': 'album is empty'})

    def test_get_last_image_for_not_forced_album(self) -> None:
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        self.create_app_and_client_with_forced_album("album2")

        response = self.test_client.get("/albums/album1/last_image")
        json_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json_response, {"error": "Illegal operation. The only accessible album is album2."})

    def test_get_last_image_for_album_after_adding_image(self) -> None:
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")

        json_response = self.test_client.get("/albums/album1/last_image").json()
        self.assertEqual(json_response, {
            'last_image_url': "/static/albums/album1/images/image0001.png"

        })

    def test_get_last_image_for_album_after_adding_two_images(self) -> None:
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")

        json_response = self.test_client.get("/albums/album1/last_image").json()
        self.assertEqual(json_response, {
            'last_image_url': "/static/albums/album1/images/image0002.png"
        })


if __name__ == '__main__':
    unittest.main()
