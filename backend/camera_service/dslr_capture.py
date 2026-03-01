import subprocess

from .errors import ImageCaptureError
from .utils import get_common_ffplay_parameters, show_overlay, stop_process


def show_dslr_preview() -> None:
    gphoto2_command = "gphoto2 --capture-movie 200 --stdout"
    common_ffplay_parameters = " ".join(get_common_ffplay_parameters())
    ffplay_command = f"ffplay -fs -fflags nobuffer -flags low_delay -framedrop -vf setpts=0 {common_ffplay_parameters} -f mjpeg -i - -autoexit"

    full_command = f"{gphoto2_command} | {ffplay_command}"
    subprocess.run(
        full_command,
        shell=True,
        check=False,
    )


def configure_dslr_capture_target() -> None:
    # Save captures to the camera card so the raw file remains on the camera.
    command_result = subprocess.run(
        ["gphoto2", "--set-config", "capturetarget=1"],
        check=False,
        capture_output=True,
        text=True,
    )
    if command_result.returncode != 0:
        raise ImageCaptureError("Image was not captured")


def capture_dslr_still(base_image_path: str) -> None:
    # Download the image for the app while keeping the raw file on the camera.
    command_result = subprocess.run(
        ["gphoto2", "--capture-image-and-download", "--filename", f"{base_image_path}.%C", "--keep-raw"],
        check=False,
        capture_output=True,
        text=True,
    )

    if command_result.returncode != 0:
        raise ImageCaptureError("Image was not captured")


def capture_dslr_image(base_image_path: str) -> None:
    try:
        overlay_process = show_overlay()
    except OSError:
        overlay_process = None

    try:
        show_dslr_preview()
        configure_dslr_capture_target()
        capture_dslr_still(base_image_path)
    finally:
        stop_process(overlay_process)
