from backend.core.config import Config


def _base_config(albums_dir: str) -> Config:
    return Config.model_validate({
        "albums": {
            "albums_dir": albums_dir
        },
        "wifi_qr_code": {
            "enabled": False
        }
    })


def create_fast_dummy_config(albums_dir: str) -> Config:
    config = _base_config(albums_dir)
    config.camera.camera_type = "dummy"
    config.camera.dummy_config.width = 120
    config.camera.dummy_config.height = 80
    config.camera.dummy_config.number_of_circles = 5
    config.camera.dummy_config.min_circle_radius = 5
    config.camera.dummy_config.max_circle_radius = 15
    return config


def create_faulty_dummy_config(albums_dir: str) -> Config:
    config = create_fast_dummy_config(albums_dir)
    config.camera.dummy_config.should_fail = True
    config.camera.dummy_config.error_message = "This is a test error message"
    config.camera.verbose_errors = False
    return config
