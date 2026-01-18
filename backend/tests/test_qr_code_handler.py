import os
import unittest
import tempfile
from pyzbar.pyzbar import decode
from PIL import Image
from backend.qr_code_api.qr_code_handler import QrCodeHandler
from backend.settings import WifiSettings
from .test_utils import temp_dir_relpath


class QrCodeHandlerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.static_test_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_test_dir_name = temp_dir_relpath(self.static_test_dir)
        self.qr_code_handler = QrCodeHandler(self.static_test_dir_name)

    def tearDown(self) -> None:
        self.static_test_dir.cleanup()  # Remove directory from file system

    def print_zbar_error_message(self) -> None:
        print("-----------------------------")
        print("Could not decode qr code using zbar.")
        print("To install zbar correctly, go to https://pypi.org/project/pyzbar/")
        print("-----------------------------")

    def test_empty_list_is_returned_when_no_qr_codes(self) -> None:
        qr_codes = self.qr_code_handler.get_qr_codes()
        self.assertEqual(qr_codes, [])

    def test_qr_code_is_returned_after_code_is_created(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_codes = self.qr_code_handler.get_qr_codes()
        self.assertEqual(len(qr_codes), 1)
        self.assertEqual(qr_codes[0].get_name(), "test_url_qr_code")

    def test_create_two_qr_codes(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code2",
            "www.test2.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_codes = self.qr_code_handler.get_qr_codes()

        self.assertEqual(len(qr_codes), 2)
        self.assertEqual(qr_codes[0].get_name(), "test_url_qr_code")
        self.assertEqual(qr_codes[1].get_name(), "test_url_qr_code2")

    def test_qr_code_file_is_created(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        expected_qr_code_path = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "test_url_qr_code.png"
        )
        self.assertTrue(os.path.exists(expected_qr_code_path))

    def test_get_relative_url_of_qr_code(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.assertEqual(
            self.qr_code_handler.get_qr_codes()[0].get_relative_url(),
            "qr_codes/test_url_qr_code.png"
        )

    def test_generated_url_qr_code_is_correct(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "test_url_qr_code.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(qr_code_text, "www.test.com")

    def test_generated_wifi_qr_code_is_correct(self) -> None:
        self.qr_code_handler.add_wifi_qr_code(
            "wifi_qr_code",
            "my_netwok_ssid",
            "WPA/WPA2",
            "my_super_secret_password",
            "Scan this qr code to connect to the wifi!"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "wifi_qr_code.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(
            qr_code_text,
            "WIFI:S:my_netwok_ssid;T:WPA/WPA2;P:my_super_secret_password;;"
        )

    def test_generate_url_qr_code_with_center_image(self) -> None:
        self.qr_code_handler = QrCodeHandler(self.static_test_dir_name, use_center_images=True)
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "test_url_qr_code.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(qr_code_text, "www.test.com")

    def test_generated_wifi_qr_code_with_center_image(self) -> None:
        self.qr_code_handler = QrCodeHandler(self.static_test_dir_name, use_center_images=True)
        self.qr_code_handler.add_wifi_qr_code(
            "wifi_qr_code",
            "my_netwok_ssid",
            "WPA/WPA2",
            "my_super_secret_password",
            "Scan this qr code to connect to the wifi!"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "wifi_qr_code.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(
            qr_code_text,
            "WIFI:S:my_netwok_ssid;T:WPA/WPA2;P:my_super_secret_password;;"
        )

    def test_get_qr_code_urls_as_strings_with_one_qr_code(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.assertEqual(
            self.qr_code_handler.get_qr_code_urls_as_strings("localhost"),
            ['For accessing test_url_qr_code : http://localhost:5000/static/qr_codes/test_url_qr_code.png']
        )

    def test_get_qr_code_urls_as_strings_with_two_qr_codes(self) -> None:
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.qr_code_handler.add_wifi_qr_code(
            "wifi_qr_code",
            "my_netwok_ssid",
            "WPA/WPA2",
            "my_super_secret_password",
            "Scan this qr code to connect to the wifi!"
        )
        self.assertEqual(
            self.qr_code_handler.get_qr_code_urls_as_strings("localhost"),
            ['For accessing test_url_qr_code : http://localhost:5000/static/qr_codes/test_url_qr_code.png',
             'For accessing wifi_qr_code : http://localhost:5000/static/qr_codes/wifi_qr_code.png']
        )

    def test_create_qr_code_handler_when_wifi_is_disabled(self) -> None:
        # We need to go down a directory to isolate from any repo config
        os.chdir(self.static_test_dir_name)

        qr_code_handler = QrCodeHandler.create_qr_code_handler_with_qr_codes(
            self.static_test_dir_name,
            5000,
            "192.168.0.1",
            wifi_settings=WifiSettings(enabled=False)
        )
        qr_codes = qr_code_handler.get_qr_codes()
        self.assertEqual(len(qr_codes), 1)
        self.assertEqual(qr_codes[0].get_name(), "start_page_url")
        os.chdir("./..")

    def test_qr_code_created_with_forced_album(self) -> None:
        os.chdir(self.static_test_dir_name)

        QrCodeHandler.create_qr_code_handler_with_qr_codes(
            self.static_test_dir_name,
            5000,
            "192.168.0.1",
            forced_album_name="album1"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "start_page_url.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(
            qr_code_text,
            "http://5000:192.168.0.1/album/album1"
        )

        os.chdir("./..")

    def test_create_qr_code_handler_when_wifi_is_enabled(self) -> None:
        # We need to go down a directory to isolate from any repo config
        os.chdir(self.static_test_dir_name)

        wifi_settings = WifiSettings(
            enabled=True,
            name="my_wifi_SSID",
            protocol="WPA/WPA2",
            password="my_super_secret_password",
            description="Scan qr code to connect to my_wifi_SSID!"
        )

        qr_code_handler = QrCodeHandler.create_qr_code_handler_with_qr_codes(
            self.static_test_dir_name,
            5000,
            "192.168.0.1",
            wifi_settings=wifi_settings
        )
        qr_codes = qr_code_handler.get_qr_codes()
        self.assertEqual(len(qr_codes), 2)
        self.assertEqual(qr_codes[0].get_name(), "wifi_qr_code")
        self.assertEqual(qr_codes[1].get_name(), "start_page_url")

        os.chdir("./..")


if __name__ == '__main__':
    unittest.main()
