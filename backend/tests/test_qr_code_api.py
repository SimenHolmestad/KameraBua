import unittest
import tempfile
from fastapi.testclient import TestClient
from backend.app import create_app
from scripts.shared import qr_code_utils
from .camera_modules_for_testing import create_fast_dummy_config
from .test_utils import temp_dir_relpath


class QrCodeApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary static dir which is deleted after every test
        self.static_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_dir_name = temp_dir_relpath(self.static_dir)
        config = create_fast_dummy_config()

        self.qr_code_context = qr_code_utils.create_qr_code_context(self.static_dir_name)
        app = create_app(
            self.static_dir_name,
            config,
            qr_code_utils.get_qr_codes(self.qr_code_context)
        )
        self.test_client = TestClient(app)

    def tearDown(self) -> None:
        self.static_dir.cleanup()

    def test_response_when_no_qr_codes_added(self) -> None:
        response = self.test_client.get("/qr_codes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"qr_codes": []})

    def test_response_after_adding_url_qr_code(self) -> None:
        qr_code_utils.add_url_qr_code(
            self.qr_code_context,
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        json_response = self.test_client.get("/qr_codes/").json()
        self.assertEqual(json_response, {
            'qr_codes': [
                {
                    'name': 'test_url_qr_code',
                    'information': 'Scan this qr code to go to www.test.com!',
                    'url': '/static/qr_codes/test_url_qr_code.png'
                }
            ]
        })

    def test_response_after_adding_url_and_wifi_qr_code(self) -> None:
        qr_code_utils.add_url_qr_code(
            self.qr_code_context,
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_code_utils.add_wifi_qr_code(
            self.qr_code_context,
            "wifi_qr_code",
            "my_netwok_ssid",
            "WPA/WPA2",
            "my_super_secret_password",
            "Scan this qr code to connect to the wifi!"
        )
        json_response = self.test_client.get("/qr_codes/").json()
        self.assertEqual(json_response, {
            'qr_codes': [
                {
                    'information': 'Scan this qr code to go to www.test.com!',
                    'name': 'test_url_qr_code',
                    'url': '/static/qr_codes/test_url_qr_code.png'
                }, {
                    'information': 'Scan this qr code to connect to the wifi!',
                    'name': 'wifi_qr_code',
                    'url': '/static/qr_codes/wifi_qr_code.png'
                }
            ]
        })
