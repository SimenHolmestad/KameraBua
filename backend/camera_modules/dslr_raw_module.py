from typing import Any, Optional
import gphoto2 as gp
from .base_dslr_module import BaseDSLRModule


class DSLRRawModule(BaseDSLRModule):
    """A dslr module where raw images are stored on the SD card of the
    camera, but not on the Raspberry PI
    """

    def __init__(self) -> None:
        super().__init__()

        # To get both raw images and jpg images, the capture target
        # needs to be 1 so that both images are transferred to the
        # camera's SD card
        self.set_capture_target(1)

    def capture_dslr_image(self, camera: Any, image_path: str, raw_image_path: Optional[str] = None) -> None:
        # camera.capture returns the file path of the raw image
        camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

        # We let the raw file stay at the SD card of the camera so we
        # do not use time to transfer it to the Raspberry PI.

        # The jpg filename is the same as raw but with .JPG extension
        jpg_filename = camera_file_path.name.replace("CR2", "JPG")

        # Transfer the jpg file from the camera to image_path
        self.save_jpg_file(image_path, camera, camera_file_path.folder, jpg_filename)
