import os
import shutil
from PIL import Image

MAX_THUMBNAIL_SIZE = (600, 600)


def _create_thumbnail(input_path: str, output_path: str) -> None:
    image = Image.open(input_path)
    image = image.convert("RGB")
    image.thumbnail(MAX_THUMBNAIL_SIZE)
    image.save(output_path)


def create_thumbnail_for_image(
    images_path: str,
    thumbnails_path: str,
    base_image_name: str
) -> None:
    image_path = _image_path_for_base_name(images_path, base_image_name)
    thumbnail_filename = base_image_name + ".jpg"
    thumbnail_path = os.path.join(thumbnails_path, thumbnail_filename)
    _create_thumbnail(image_path, thumbnail_path)

def recreate_all_thumbnails(images_path: str, thumbnails_path: str) -> None:
    shutil.rmtree(thumbnails_path)
    os.mkdir(thumbnails_path)
    image_names = sorted(os.listdir(images_path))
    for name in image_names:
        base_name, extension = os.path.splitext(name)
        if not extension:
            continue
        create_thumbnail_for_image(images_path, thumbnails_path, base_name)


def _image_path_for_base_name(images_path: str, base_image_name: str) -> str:
    for extension in (".jpg", ".jpeg", ".png"):
         if os.path.exists(os.path.join(images_path, base_image_name + extension)):
             return os.path.join(images_path, base_image_name + extension)

    raise RuntimeError(f"Could not find image for base name {base_image_name} in path {images_path}")

