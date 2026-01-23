from backend.core.config import Config


def _base_config() -> Config:
    return Config.model_validate({
        "wifi_qr_code": {
            "enabled": False
        }
    })


def create_fast_dummy_config() -> Config:
    config = _base_config()
    config.camera.module = "dummy"
    config.camera.options = {
        "width": 120,
        "height": 80,
        "number_of_circles": 5,
        "min_circle_radius": 5,
        "max_circle_radius": 15
    }
    return config


def create_faulty_dummy_config() -> Config:
    config = create_fast_dummy_config()
    config.camera.options.update({
        "should_fail": True,
        "error_message": "This is a test error message",
        "verbose_errors": False
    })
    return config


def create_dummy_raw_config() -> Config:
    config = create_fast_dummy_config()
    config.camera.modules["dummy"]["needs_raw_file_transfer"] = True
    config.camera.modules["dummy"]["raw_file_extension"] = ".cr2"
    return config
