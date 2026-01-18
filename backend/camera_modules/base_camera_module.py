from abc import ABC, abstractmethod
import traceback
from typing import Optional


class BaseCameraModule(ABC):
    """Abstract class containing common image capture related code"""

    def __init__(self,
                 file_extension: str,
                 needs_raw_file_transfer: bool = False,
                 raw_file_extension: Optional[str] = None,
                 verbose_errors: bool = True) -> None:
        """needs_raw_file_transfer should only be True if the camera captures
        both jpg and raw and the raw file needs to be stored in the system"""
        self.file_extension = file_extension
        self.needs_raw_file_transfer = needs_raw_file_transfer
        self.raw_file_extension = raw_file_extension
        self.verbose_errors = verbose_errors
        self.is_busy = False

    @abstractmethod
    def capture_image(self, image_path: str, raw_file_path: Optional[str] = None) -> None:
        """Method for capturing image and storing it in image_path. Should
        raise ImageCaptureError with and error message if something
        goes wrong with capture.

        The raw_file_path will only be neeeded if
        needs_raw_file_transfer is set to true and raw_file_extension
        is given.
        """
        pass

    def try_capture_image(self, image_path: str, raw_file_path: Optional[str] = None) -> None:
        if self.is_busy:
            raise ImageCaptureError("Camera is already in use")
        self.is_busy = True

        try:
            self.capture_image(image_path, raw_file_path)
        except Exception as e:
            self.__handle_exception(e)
        finally:
            self.is_busy = False

    def __handle_exception(self, e: Exception) -> None:
        if self.verbose_errors:
            traceback.print_exc()

        if not isinstance(e, ImageCaptureError):
            raise ImageCaptureError("Something went wrong during image capture")

        raise e


class ImageCaptureError(RuntimeError):
    pass
