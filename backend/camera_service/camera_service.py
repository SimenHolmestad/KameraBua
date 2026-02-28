import traceback

from backend.core.config import CameraConfig
from .dummy_image_generator import create_dummy_image
from .dslr_capture import capture_dslr_image
from .rpicam_capture import capture_rpicam_image
from .errors import ImageCaptureError


class CameraService:
    def __init__(self, camera_config: CameraConfig) -> None:
        self.camera_config = camera_config
        self._busy = False

    def capture_image(self, base_image_path: str) -> None:
        if self._busy:
            raise ImageCaptureError("Camera is already in use")

        self._busy = True
        try:
            if self.camera_config.camera_type == "dummy":
                create_dummy_image(self.camera_config.dummy_config, base_image_path)
            elif self.camera_config.camera_type == "rpicam":
                capture_rpicam_image(base_image_path)
            elif self.camera_config.camera_type == "dslr":
                capture_dslr_image(base_image_path)
            else:
                raise ImageCaptureError(f"Unsupported camera type: {self.camera_config.camera_type}")
        except Exception as exc:
            self._handle_exception(exc)
        finally:
            self._busy = False

    def _handle_exception(self, exc: Exception) -> None:
        if self.camera_config.verbose_errors:
            traceback.print_exc()

        if not isinstance(exc, ImageCaptureError):
            raise ImageCaptureError("Something went wrong during image capture") from exc

        raise exc
