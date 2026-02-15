import os
import shutil
from PIL import Image
from .image_name_formatter import change_extension_of_filename

MAX_THUMBNAIL_SIZE = (600, 600)


def _create_thumbnail(input_path: str, output_path: str) -> None:
    image = Image.open(input_path)
    image = image.convert("RGB")
    image.thumbnail(MAX_THUMBNAIL_SIZE)
    image.save(output_path)


def create_thumbnail_for_image(
    images_path: str,
    thumbnails_path: str,
    image_name: str
) -> None:
    thumbnail_name = change_extension_of_filename(image_name, ".jpg")
    thumbnail_path = os.path.join(thumbnails_path, thumbnail_name)
    image_path = os.path.join(images_path, image_name)
    _create_thumbnail(image_path, thumbnail_path)


def recreate_all_thumbnails(images_path: str, thumbnails_path: str) -> None:
    shutil.rmtree(thumbnails_path)
    os.mkdir(thumbnails_path)
    image_names = sorted(os.listdir(images_path))
    for name in image_names:
        create_thumbnail_for_image(images_path, thumbnails_path, name)
