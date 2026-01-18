from typing import Any
import gphoto2 as gp
from .base_dslr_module import BaseDSLRModule


class DSLRRawTransferModule(BaseDSLRModule):
    """A dslr module where raw images are stored on the Raspberry PI"""

    def __init__(self) -> None:
        super().__init__(needs_raw_file_transfer=True, raw_file_extension=".cr2")

        # To get both raw images and jpg images, the capture target
        # needs to be 1 so that both images are transferred to the
        # camera's SD card
        self.set_capture_target(1)

    def capture_dslr_image(self, camera: Any, image_path: str, raw_image_path: str) -> None:
        # camera.capture returns the file path of the raw image
        camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

        if "CR2" in camera_file_path.name:
            self.save_raw_image(raw_image_path, camera, camera_file_path)

        # The jpg filename is the same as raw but with .JPG extension
        jpg_filename = camera_file_path.name.replace("CR2", "JPG")

        # Transfer the jpg file from the camera to image_path
        self.save_jpg_file(image_path, camera, camera_file_path.folder, jpg_filename)
