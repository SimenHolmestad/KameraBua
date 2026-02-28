import unittest
from pydantic import ValidationError
from backend.core.config import Config


class ConfigTestCase(unittest.TestCase):
    def test_albums_dir_must_start_with_backend_static(self) -> None:
        with self.assertRaises(ValidationError):
            Config.model_validate({
                "albums": {
                    "albums_dir": "static/albums"
                }
            })

    def test_albums_dir_accepts_backend_static_prefix(self) -> None:
        config = Config.model_validate({
            "albums": {
                "albums_dir": "backend/static/custom_albums"
            }
        })
        self.assertEqual(config.albums.albums_dir, "backend/static/custom_albums")

    def test_albums_dir_normalizes_windows_separator(self) -> None:
        config = Config.model_validate({
            "albums": {
                "albums_dir": "backend\\static\\windows_albums"
            }
        })
        self.assertEqual(config.albums.albums_dir, "backend/static/windows_albums")

    def test_camera_type_accepts_supported_values(self) -> None:
        config = Config.model_validate({
            "albums": {"albums_dir": "backend/static/custom_albums"},
            "camera": {"camera_type": "rpicam"}
        })
        self.assertEqual(config.camera.camera_type, "rpicam")

    def test_camera_type_rejects_invalid_value(self) -> None:
        with self.assertRaises(ValidationError):
            Config.model_validate({
                "albums": {"albums_dir": "backend/static/custom_albums"},
                "camera": {"camera_type": "unknown_type"}
            })

    def test_dummy_config_has_defaults(self) -> None:
        config = Config.model_validate({
            "albums": {"albums_dir": "backend/static/custom_albums"}
        })
        self.assertEqual(config.camera.dummy_config.width, 1200)
        self.assertEqual(config.camera.dummy_config.height, 800)
        self.assertEqual(config.camera.dummy_config.number_of_circles, 80)

    def test_dslr_config_valid_without_raw_transfer_settings(self) -> None:
        config = Config.model_validate({
            "albums": {"albums_dir": "backend/static/custom_albums"},
            "camera": {
                "camera_type": "dslr"
            }
        })
        self.assertEqual(config.camera.camera_type, "dslr")


if __name__ == '__main__':
    unittest.main()
