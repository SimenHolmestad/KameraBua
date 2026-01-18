import os
import shutil
import socket
import platform
import subprocess
from typing import Any, Optional
from backend.qr_code_api.qr_code_handler import QrCodeHandler
from backend.camera_module_options import get_instance_of_camera_module_by_name
from backend.album_storage.folder_album_handler import FolderAlbumHandler
from backend.app import create_app
from backend.settings import Settings

STATIC_FOLDER_NAME = "static"
DEBUG_PORT = 3000
PRODUCTION_PORT = 5000


def static_folder_path(static_folder_name: str = STATIC_FOLDER_NAME) -> str:
    return os.path.join("backend", static_folder_name)


def build_frontend(static_folder_name: str = STATIC_FOLDER_NAME) -> None:
    os.chdir("frontend")
    _run_npm_build_commands()
    _move_frontend_folder_to_flask(static_folder_name)
    os.chdir("./..")


def frontend_is_built(static_folder_name: str = STATIC_FOLDER_NAME) -> bool:
    node_modules_path = os.path.join(
        "frontend",
        "node_modules"
    )
    build_folder_path = os.path.join(
        "backend",
        static_folder_name,
        "react"
    )
    return os.path.exists(node_modules_path) and os.path.exists(build_folder_path)


def open_webpage_in_device_browser(url: str) -> Optional[subprocess.Popen]:
    """If chromium is used, the chromium subprocess is returned so that it can be terminated later."""
    if os.path.exists("/usr/bin/chromium-browser"):
        os.environ["DISPLAY"] = ":0"
        cmd = ["sleep", "2", "&&", "/usr/bin/chromium-browser", "--start-fullscreen", url]
        # Return a chromium subprocessed with suppressed output
        with open(os.devnull, 'w') as fp:
            return subprocess.Popen(" ".join(cmd), shell=True, stdout=fp, stderr=fp)
    if platform.system() == "Darwin":
        cmd = "open " + url
        subprocess.run(cmd, shell=True)
    return None


def create_qr_code_handler(
    settings: Settings,
    host_ip: str,
    port: int,
    static_folder_name: str = STATIC_FOLDER_NAME
) -> QrCodeHandler:
    return QrCodeHandler.create_qr_code_handler_with_qr_codes(
        static_folder_path(static_folder_name),
        host_ip,
        port,
        use_center_images=settings.qr_codes.use_center_images,
        forced_album_name=settings.albums.forced_album,
        wifi_settings=settings.qr_codes.wifi
    )


def get_url_for_qr_code_page(host_ip: str, port: int, forced_album: Optional[str]) -> str:
    if forced_album:
        return "http://{}:{}/album/{}/last_image_qr".format(
            host_ip,
            str(port),
            forced_album
        )
    return "http://{}:{}/qr".format(host_ip, str(port))


def get_camera_module_instance(settings: Settings) -> Any:
    return get_instance_of_camera_module_by_name(settings.camera.module)


def get_album_handler_instance(static_folder_name: str = STATIC_FOLDER_NAME) -> FolderAlbumHandler:
    return FolderAlbumHandler(static_folder_path(static_folder_name), "albums")


def ensure_forced_album_is_created(
    album_handler: FolderAlbumHandler,
    forced_album: Optional[str]
) -> None:
    if forced_album:
        album_handler.get_or_create_album(forced_album)


def create_app_with_settings(
    settings: Settings,
    host_ip: str,
    port: int,
    static_folder_name: str = STATIC_FOLDER_NAME
) -> Any:
    qr_code_handler = create_qr_code_handler(settings, host_ip, port, static_folder_name)
    album_handler = get_album_handler_instance(static_folder_name)
    ensure_forced_album_is_created(album_handler, settings.albums.forced_album)
    camera_module = get_camera_module_instance(settings)

    return create_app(
        album_handler,
        static_folder_name,
        camera_module,
        qr_code_handler,
        forced_album_name=settings.albums.forced_album
    )


def find_ip_address_for_device() -> str:
    """Returns the IP address for this device."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def _run_npm_build_commands() -> None:
    with open(os.devnull, 'w') as fp:
        print("Installing react dependencies...")
        subprocess.run("npm install", shell=True, stdout=fp)
        print("Building react application...")
        subprocess.run("npm run build", shell=True, stdout=fp)


def _move_frontend_folder_to_flask(static_folder_name: str) -> None:
    print("moving build folder to flask...")
    target_path = os.path.join("./..", "backend", static_folder_name, "react")
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.move("./build", target_path)
