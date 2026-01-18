from abc import ABC, abstractmethod
from typing import Any, List


class BaseAlbumHandler(ABC):
    """Base class for creating Album Class instances"""

    @abstractmethod
    def get_available_album_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_album(self, album_name: str) -> Any:
        pass

    @abstractmethod
    def get_or_create_album(self, album_name: str, description: str = "") -> Any:
        pass

    @abstractmethod
    def ensure_all_thumbnails_correct(self) -> None:
        pass

    @abstractmethod
    def album_exists(self, album_name: str) -> bool:
        pass
