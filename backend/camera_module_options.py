from typing import Any, Dict, List, Type
from .camera_modules.dummy_camera_module import DummyCameraModule
from .camera_modules.rpicam_module import RPICameraModule

CAMERA_MODULE_OPTIONS: Dict[str, Type] = {
    "dummy": DummyCameraModule,
    "rpicam": RPICameraModule
}

# The dslr modules can only be imported when gphoto2 is installed.
try:
    from .camera_modules.dslr_jpg_module import DSLRJpgModule
    from .camera_modules.dslr_raw_module import DSLRRawModule
    from .camera_modules.dslr_raw_transfer_module import DSLRRawTransferModule
    CAMERA_MODULE_OPTIONS["dslr_jpg"] = DSLRJpgModule
    CAMERA_MODULE_OPTIONS["dslr_raw"] = DSLRRawModule
    CAMERA_MODULE_OPTIONS["dslr_raw_transfer"] = DSLRRawTransferModule
except ModuleNotFoundError:
    print("DLSR modules cannot be used as gphoto2 is not available.")
    print("See intructions on how to install gphoto2 in readme.")


class CameraModuleNotFoundError(Exception):
    pass


def get_camera_module_name_options() -> List[str]:
    """Returns a list with the names of the possible camera modules the
    system can use."""
    return list(CAMERA_MODULE_OPTIONS.keys())


def get_instance_of_camera_module_by_name(module_name: str) -> Any:
    if module_name not in get_camera_module_name_options():
        raise CameraModuleNotFoundError

    return CAMERA_MODULE_OPTIONS[module_name]()
