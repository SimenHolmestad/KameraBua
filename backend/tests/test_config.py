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


if __name__ == '__main__':
    unittest.main()
