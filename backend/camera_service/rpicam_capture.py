import os
import subprocess
from .errors import ImageCaptureError


def capture_rpicam_image(base_image_path: str) -> None:
    image_path = base_image_path + ".jpg"
    subprocess.run(["rpicam-still", "-f", "--vflip", "-o", image_path], check=False)
    if not os.path.exists(image_path):
        raise ImageCaptureError("Image was not captured")

