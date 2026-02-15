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
    config.camera.module = "dummy"
    config.camera.options = {
        "width": 120,
        "height": 80,
        "number_of_circles": 5,
        "min_circle_radius": 5,
        "max_circle_radius": 15
    }
    return config


def create_faulty_dummy_config(albums_dir: str) -> Config:
    config = create_fast_dummy_config(albums_dir)
    config.camera.options.update({
        "should_fail": True,
        "error_message": "This is a test error message",
        "verbose_errors": False
    })
    return config
