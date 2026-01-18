from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseAlbum(ABC):
    """Base class for album-related storage of images"""

    @abstractmethod
    def get_album_description(self) -> str:
        pass

    @abstractmethod
    def set_album_description(self, content: str) -> None:
        pass

    @abstractmethod
    def get_relative_url_of_last_image(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_relative_urls_of_all_images(self) -> List[str]:
        pass

    @abstractmethod
    def get_relative_urls_of_all_thumbnails(self) -> List[str]:
        pass

    @abstractmethod
    def try_capture_image_to_album(self, camera_module: Any) -> None:
        pass

    @abstractmethod
    def ensure_thumbnails_correct(self) -> None:
        pass
