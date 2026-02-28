import subprocess
from .errors import ImageCaptureError


def capture_dslr_image(base_image_path: str) -> None:
    subprocess.run(
        "gphoto2 --capture-movie 200 --stdout | ffplay -fs -loglevel warning -fflags nobuffer -flags low_delay -framedrop -vf setpts=0 -probesize 5000000 -analyzeduration 1000000 -f mjpeg -i - -autoexit",
        shell=True,
        check=False,
    )

    # Save captures to the camera card so the raw file remains on the camera.
    subprocess.run(
        "gphoto2 --set-config capturetarget=1",
        shell=True,
        check=False,
    )

    # Download the image for the app while keeping the raw file on the camera.
    command_result = subprocess.run(
        f"gphoto2 --capture-image-and-download --filename {base_image_path}.%C --keep-raw",
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )

    if command_result.returncode != 0:
        raise ImageCaptureError("Image was not captured")
