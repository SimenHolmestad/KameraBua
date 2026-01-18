from shutil import copyfile
from typing import Optional
from backend.camera_modules.dummy_camera_module import DummyCameraModule
from backend.camera_modules.base_camera_module import BaseCameraModule, ImageCaptureError


def create_fast_dummy_module() -> DummyCameraModule:
    """Creates a faster dummy module for quicker test runs"""
    return DummyCameraModule(
        width=120,
        height=80,
        number_of_circles=5,
        min_circle_radius=5,
        max_circle_radius=15
    )


class FaultyCameraModule(BaseCameraModule):
    """A camera module to test error handling functionality"""

    def __init__(self, should_fail: bool = True) -> None:
        super().__init__(".jpg", verbose_errors=False)
        self.should_fail = should_fail
        self.dummy_module = create_fast_dummy_module()

    def capture_image(self, image_path: str, raw_file_path: Optional[str] = None) -> None:
        if self.should_fail:
            raise ImageCaptureError("This is a test error message")

        self.dummy_module.try_capture_image(image_path)


class DummyRawModule(BaseCameraModule):
    """Dummy module which also creates dummy raw files.

    The module uses another dummy module for creating the image file
    before renaming and moving the file to the raw directory.
    """

    def __init__(self) -> None:
        super().__init__(".png", needs_raw_file_transfer=True, raw_file_extension=".cr2")
        self.dummy_module = create_fast_dummy_module()

    def capture_image(self, image_path: str, raw_file_path: str) -> None:
        self.dummy_module.try_capture_image(image_path)
        copyfile(image_path, raw_file_path)
