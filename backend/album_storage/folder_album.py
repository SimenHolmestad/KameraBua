from typing import Any, List, Optional
from PIL import Image
from .base_album import BaseAlbum
from .folder import Folder
from .image_name_formatter import ImageNameFormatter
from .current_image_tracker import CurrentImageTracker
MAX_THUMBNAIL_SIZE = (600, 600)


class FolderAlbum(BaseAlbum):
    """An Album implementation where all album-related information is
    stored in a single folder.
    """

    def __init__(
        self,
        album_name: str,
        album_folder_container: Folder,
        image_name_prefix: str = "image"
    ) -> None:
        self.album_folder_container: Folder = album_folder_container
        self.album_folder: Folder = Folder(album_folder_container.get_path(), album_name)
        self.images_folder: Folder = Folder(self.album_folder.get_path(), "images")
        self.thumbnails_folder: Folder = Folder(self.album_folder.get_path(), "thumbnails")
        self.image_name_formatter: ImageNameFormatter = ImageNameFormatter(image_name_prefix)
        self.current_image_tracker: CurrentImageTracker = CurrentImageTracker(
            self.album_folder,
            self.images_folder,
            self.image_name_formatter
        )

    def get_album_description(self) -> str:
        if not self.album_folder.file_exists_in_folder("description.txt"):
            return ""

        return self.album_folder.read_file_in_folder("description.txt")

    def set_album_description(self, content: str) -> None:
        self.album_folder.write_file_in_folder("description.txt", content)

    def get_relative_url_of_last_image(self) -> Optional[str]:
        """Returns the url of the last image captured to the album."""
        last_image_filename = self.current_image_tracker.get_name_of_last_image()
        if not last_image_filename:
            return None  # This means album is empty

        return self.__get_relative_url_to_file_in_folder(self.images_folder, last_image_filename)

    def get_relative_url_of_last_thumbnail(self) -> Optional[str]:
        """Returns the url of the last thumbnail captured to the album."""
        last_image_filename = self.current_image_tracker.get_name_of_last_image()
        if not last_image_filename:
            return None  # This means album is empty

        thumbnail_filename = self.__convert_image_name_to_thumbnail_name(last_image_filename)
        return self.__get_relative_url_to_file_in_folder(self.thumbnails_folder, thumbnail_filename)

    def get_relative_urls_of_all_images(self) -> List[str]:
        return self.__get_relative_urls_to_all_files_in_folder(
            self.images_folder
        )

    def get_relative_urls_of_all_thumbnails(self) -> List[str]:
        return self.__get_relative_urls_to_all_files_in_folder(
            self.thumbnails_folder
        )

    def try_capture_image_to_album(self, camera_module: Any) -> None:
        """Tries to capture an image to the album using the specified camera
        module.

        As this method will call the try_capture_image method of the
        camera_module, an ImageCaptureError might be raised.
        """
        next_image_name = self.__get_next_image_name_with_extension(camera_module.file_extension)

        if camera_module.needs_raw_file_transfer:
            self.__try_capture_image_with_raw_file_transfer(camera_module)
        else:
            self.__try_capture_image(camera_module)

        self.__create_thumbnail_for_image(next_image_name)
        self.current_image_tracker.increase_image_number()

    def ensure_thumbnails_correct(self) -> None:
        self.thumbnails_folder.create_folder_if_not_exist()

        number_of_images = self.images_folder.count_files()
        number_of_thumbnails = self.thumbnails_folder.count_files()
        if not number_of_images == number_of_thumbnails:
            self.recreate_all_thumbnails()

    def recreate_all_thumbnails(self) -> None:
        self.thumbnails_folder.remove_all_folder_content()

        image_names = self.images_folder.get_folder_contents()
        for name in image_names:
            self.__create_thumbnail_for_image(name)

    def __create_thumbnail(self, input_path: str, output_path: str) -> None:
        image = Image.open(input_path)
        image = image.convert('RGB')
        image.thumbnail(MAX_THUMBNAIL_SIZE)
        image.save(output_path)

    def __create_thumbnail_for_image(self, image_name: str) -> None:
        # All thumbnails are saved as .jpg
        thumbnail_name = self.__convert_image_name_to_thumbnail_name(image_name)
        thumbnail_path = self.thumbnails_folder.get_path_to_file(thumbnail_name)
        image_path = self.images_folder.get_path_to_file(image_name)
        self.__create_thumbnail(image_path, thumbnail_path)

    def __convert_image_name_to_thumbnail_name(self, image_name: str) -> str:
        return self.image_name_formatter.change_extension_of_filename(image_name, ".jpg")

    def __get_relative_url_to_file_in_folder(self, folder: Folder, filename: str) -> str:
        """Returns the url relative to the album folder container"""
        return "{}/{}/{}/{}".format(
            self.album_folder_container.get_name(),
            self.album_folder.get_name(),
            folder.get_name(),
            filename
        )

    def __get_relative_urls_to_all_files_in_folder(self, folder: Folder) -> List[str]:
        filenames = folder.get_sorted_folder_contents()
        relative_urls = list(map(
            lambda name: self.__get_relative_url_to_file_in_folder(folder, name),
            filenames
        ))
        return relative_urls

    def __get_next_image_name_with_extension(self, extension: str) -> str:
        return self.current_image_tracker.get_next_image_name(extension)

    def __get_next_image_path(self, folder: Folder, extension: str) -> str:
        image_name = self.__get_next_image_name_with_extension(extension)
        return folder.get_path_to_file(image_name)

    def __try_capture_image_with_raw_file_transfer(self, camera_module: Any) -> None:
        raw_image_folder = Folder(self.album_folder.get_path(), "raw_images")
        raw_image_filepath = self.__get_next_image_path(raw_image_folder, camera_module.raw_file_extension)
        next_image_filepath = self.__get_next_image_path(self.images_folder, camera_module.file_extension)
        camera_module.try_capture_image(next_image_filepath, raw_image_filepath)

    def __try_capture_image(self, camera_module: Any) -> None:
        next_image_filepath = self.__get_next_image_path(self.images_folder, camera_module.file_extension)
        camera_module.try_capture_image(next_image_filepath)
