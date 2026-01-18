import time
from typing import Any, Optional
import gphoto2 as gp
from .base_dslr_module import BaseDSLRModule
from .base_camera_module import ImageCaptureError


class DSLRJpgModule(BaseDSLRModule):
    """A dslr module where no raw images are stored"""

    def __init__(self) -> None:
        super().__init__()

        # For maximum speed, we set capture target to 0, so that the
        # jpg image is not written to the SD card before being written
        # to the Raspberry PI.
        self.set_capture_target(0)

        print("---------------------------------------------------")
        print()
        print("IMPORTANT!")
        print("Make sure your camera is set to only capture .jpg")
        print("images and not raw images.")
        print()
        print("---------------------------------------------------")
        time.sleep(2)

    def capture_dslr_image(self, camera: Any, image_path: str, raw_image_path: Optional[str] = None) -> None:
        # camera.capture should return the file path of the jpg image
        camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

        if "CR2" in camera_file_path.name:
            print("Raw image captured when using JPG module!")
            print("Set camera to only capture jpg files and restart server.")
            raise ImageCaptureError("Camera was set to RAW but should have been .jpg")

        # Transfer the jpg file from the camera to image_path
        self.save_jpg_file(image_path, camera, camera_file_path.folder, camera_file_path.name)
