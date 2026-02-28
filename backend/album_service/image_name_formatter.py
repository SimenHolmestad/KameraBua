"""Helpers for formatting image names."""


def format_image_name(image_name_prefix: str, image_number: int) -> str:
    return image_name_prefix + str(image_number).rjust(4, "0")


def change_extension_of_filename(image_name: str, file_extension: str) -> str:
    return image_name.split(".")[0] + file_extension
