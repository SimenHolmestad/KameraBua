import os
import signal
import subprocess
import time
import traceback
from typing import Any, Dict, Optional
from backend.core.config import Config

DEFAULT_MODULE_NAME = "dummy"
_BUSY = False
_DSLR_INITIALIZED: Dict[str, bool] = {}


class ImageCaptureError(RuntimeError):
    pass


class CameraModuleNotFoundError(RuntimeError):
    pass


def try_capture_image(
    config: Config,
    image_path: str,
    raw_file_path: Optional[str] = None
) -> None:
    module_name = config.camera.module or DEFAULT_MODULE_NAME
    module_config = _get_module_config(config, module_name)
    capture_handler = _get_capture_handler(module_name)
    verbose_errors = config.camera.options.get("verbose_errors", True)

    global _BUSY
    if _BUSY:
        raise ImageCaptureError("Camera is already in use")
    if module_config.get("needs_raw_file_transfer") and not raw_file_path:
        raise ImageCaptureError(f"Missing raw file path for camera module: {module_name}")
    _BUSY = True

    try:
        capture_handler(config.camera.options, module_config, image_path, raw_file_path)
    except Exception as exc:
        _handle_exception(exc, verbose_errors)
    finally:
        _BUSY = False


def _handle_exception(exc: Exception, verbose_errors: bool) -> None:
    if verbose_errors:
        traceback.print_exc()

    if not isinstance(exc, ImageCaptureError):
        raise ImageCaptureError("Something went wrong during image capture") from exc

    raise exc


def _get_module_config(config: Config, module_name: str) -> Dict[str, Any]:
    modules = config.camera.modules
    if module_name not in modules:
        raise CameraModuleNotFoundError(f"Unknown camera module: {module_name}")
    return modules[module_name]


def _get_capture_handler(module_name: str) -> Any:
    handlers = {
        "dummy": _capture_dummy_image,
        "rpicam": _capture_rpicam_image,
        "dslr_jpg": _capture_dslr_jpg_image,
        "dslr_raw": _capture_dslr_raw_image,
        "dslr_raw_transfer": _capture_dslr_raw_transfer_image,
    }
    if module_name not in handlers:
        raise CameraModuleNotFoundError(f"Unknown camera module: {module_name}")
    return handlers[module_name]


def _capture_dummy_image(
    options: Dict[str, Any],
    module_config: Dict[str, Any],
    image_path: str,
    raw_file_path: Optional[str]
) -> None:
    if options.get("should_fail"):
        raise ImageCaptureError(options.get("error_message", "This is a test error message"))

    from random import randint
    import matplotlib.pyplot as plt
    import numpy as np

    width = int(options.get("width", 1200))
    height = int(options.get("height", 800))
    number_of_circles = int(options.get("number_of_circles", 80))
    min_circle_radius = int(options.get("min_circle_radius", 30))
    max_circle_radius = int(options.get("max_circle_radius", 80))

    image = np.full((height, width, 3), 255, dtype=np.uint8)
    for _ in range(number_of_circles):
        image = _add_random_circle_to_image(
            image,
            width,
            height,
            min_circle_radius,
            max_circle_radius,
            randint
        )

    plt.imsave(image_path, image)

    if module_config.get("needs_raw_file_transfer") and raw_file_path:
        _copy_file(image_path, raw_file_path)


def _add_random_circle_to_image(
    image: "Any",
    width: int,
    height: int,
    min_circle_radius: int,
    max_circle_radius: int,
    randint: Any
) -> "Any":
    x_center = randint(0, width - 1)
    y_center = randint(0, height - 1)
    radius = randint(min_circle_radius, max_circle_radius)
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)

    x_start = max(0, x_center - radius - 1)
    x_end = min(width, x_center + radius + 1)
    y_start = max(0, y_center - radius - 1)
    y_end = min(height, y_center + radius + 1)

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            if (x - x_center) ** 2 + (y - y_center) ** 2 < radius ** 2:
                image[y, x, 0] = r
                image[y, x, 1] = g
                image[y, x, 2] = b
    return image


def _capture_rpicam_image(
    options: Dict[str, Any],
    module_config: Dict[str, Any],
    image_path: str,
    raw_file_path: Optional[str]
) -> None:
    subprocess.run(["rpicam-still", "-f", "--vflip", "-o", image_path], check=False)
    if not os.path.exists(image_path):
        raise ImageCaptureError("Image was not captured")


def _capture_dslr_jpg_image(
    options: Dict[str, Any],
    module_config: Dict[str, Any],
    image_path: str,
    raw_file_path: Optional[str]
) -> None:
    gp = _require_gphoto2()
    _ensure_dslr_initialized("dslr_jpg")
    _set_capture_target(0)

    camera = gp.Camera()
    camera.init()
    print("Capturing image...")
    camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    if "CR2" in camera_file_path.name:
        print("Raw image captured when using JPG module!")
        print("Set camera to only capture jpg files and restart server.")
        camera.exit()
        raise ImageCaptureError("Camera was set to RAW but should have been .jpg")

    _save_jpg_file(gp, image_path, camera, camera_file_path.folder, camera_file_path.name)
    camera.exit()


def _capture_dslr_raw_image(
    options: Dict[str, Any],
    module_config: Dict[str, Any],
    image_path: str,
    raw_file_path: Optional[str]
) -> None:
    gp = _require_gphoto2()
    _ensure_dslr_initialized("dslr_raw")
    _set_capture_target(1)

    camera = gp.Camera()
    camera.init()
    print("Capturing image...")
    camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    jpg_filename = camera_file_path.name.replace("CR2", "JPG")
    _save_jpg_file(gp, image_path, camera, camera_file_path.folder, jpg_filename)
    camera.exit()


def _capture_dslr_raw_transfer_image(
    options: Dict[str, Any],
    module_config: Dict[str, Any],
    image_path: str,
    raw_file_path: Optional[str]
) -> None:
    gp = _require_gphoto2()
    _ensure_dslr_initialized("dslr_raw_transfer")
    _set_capture_target(1)

    if not raw_file_path:
        raise ImageCaptureError("Missing raw file path for raw transfer capture")

    camera = gp.Camera()
    camera.init()
    print("Capturing image...")
    camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    if "CR2" in camera_file_path.name:
        _save_raw_image(gp, raw_file_path, camera, camera_file_path)

    jpg_filename = camera_file_path.name.replace("CR2", "JPG")
    _save_jpg_file(gp, image_path, camera, camera_file_path.folder, jpg_filename)
    camera.exit()


def _require_gphoto2() -> Any:
    try:
        import gphoto2 as gp
    except ModuleNotFoundError as exc:
        raise CameraModuleNotFoundError(
            "gphoto2 is not available. Install gphoto2 to use DSLR camera modules."
        ) from exc
    return gp


def _ensure_dslr_initialized(module_name: str) -> None:
    if _DSLR_INITIALIZED.get(module_name):
        return
    gp = _require_gphoto2()

    camera = gp.Camera()
    print("Please connect and switch on your DSLR Camera", flush=True)
    while True:
        try:
            _kill_gphoto2_process()
            camera.init()
        except gp.GPhoto2Error as ex:
            if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                time.sleep(3)
                continue
            raise
        break
    print("DSLR Camera connected.")
    camera.exit()
    _DSLR_INITIALIZED[module_name] = True


def _kill_gphoto2_process() -> None:
    process = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, _ = process.communicate()

    for line in out.splitlines():
        if b"gvfsd-gphoto2" in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


def _set_capture_target(target_number: int) -> None:
    subprocess.run(
        f"gphoto2 --set-config capturetarget={target_number}",
        shell=True,
        check=False
    )


def _save_jpg_file(
    gp: Any,
    image_path: str,
    camera: Any,
    camera_image_folder: str,
    camera_image_filename: str
) -> None:
    camera_file = camera.file_get(
        camera_image_folder, camera_image_filename, gp.GP_FILE_TYPE_NORMAL
    )
    print("Saving jpg image to", image_path)
    camera_file.save(image_path)


def _save_raw_image(
    gp: Any,
    raw_image_path: str,
    camera: Any,
    camera_file_path: Any
) -> None:
    print("Saving raw image to", raw_image_path)
    camera_file = camera.file_get(
        camera_file_path.folder,
        camera_file_path.name,
        gp.GP_FILE_TYPE_NORMAL
    )
    camera_file.save(raw_image_path)


def _copy_file(source_path: str, target_path: str) -> None:
    with open(source_path, "rb") as source:
        with open(target_path, "wb") as target:
            target.write(source.read())
