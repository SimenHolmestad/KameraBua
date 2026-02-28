import os
import shutil
import socket
import platform
import subprocess
from typing import Any, Optional
from typing import Mapping
from scripts.shared import qr_code_utils
from backend.album_service.album_service import AlbumService
from backend.app import create_app
from backend.core.config import Config
DEBUG_PORT = 3000
PRODUCTION_PORT = 5000


def static_folder_path(static_folder_name: str) -> str:
    return os.path.join("backend", static_folder_name)


def build_frontend(static_folder_name: str) -> None:
    os.chdir("frontend")
    _run_npm_build_commands()
    _move_frontend_folder_to_backend(static_folder_name)
    os.chdir("./..")


def frontend_is_built(static_folder_name: str) -> bool:
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
    if platform.system() == "Darwin":
        cmd = "open " + url
        subprocess.run(cmd, shell=True)
        return None

    if os.path.exists("/usr/bin/chromium"):
        os.environ["DISPLAY"] = ":0"
        print("Opening chromium browser...")
        cmd = ["sleep", "2", "&&", "/usr/bin/chromium", "--start-fullscreen", url]
        # Return a chromium subprocessed with suppressed output
        with open(os.devnull, 'w') as fp:
            return subprocess.Popen(" ".join(cmd), shell=True, stdout=fp, stderr=fp)

    print("Could not open browser automatically or find chromium")


def create_qr_codes(
    config: Config,
    host_ip: str,
    port: int
) -> list[Mapping[str, str]]:
    context = qr_code_utils.create_qr_codes_with_config(
        static_folder_path(config.static_folder_name),
        host_ip,
        port,
        use_center_images=config.qr_codes.use_center_images,
        forced_album_name=config.albums.forced_album,
        wifi_config=config.wifi_qr_code
    )
    return qr_code_utils.get_qr_codes(context)


def get_url_for_qr_code_page(host_ip: str, port: int, forced_album: Optional[str]) -> str:
    if forced_album:
        return f"http://{host_ip}:{port}/album/{forced_album}/last_image_qr"
    return f"http://{host_ip}:{port}/qr"


def ensure_forced_album_is_created(
    service: AlbumService,
    forced_album: Optional[str]
) -> None:
    if forced_album:
        service.get_or_create_album(forced_album)


def create_app_with_config(
    config: Config,
    host_ip: str,
    port: int
) -> Any:
    qr_codes = create_qr_codes(config, host_ip, port)
    service = AlbumService(config.albums, config.camera)
    ensure_forced_album_is_created(service, config.albums.forced_album)

    return create_app(
        static_folder_path(config.static_folder_name),
        config,
        qr_codes
    )


def find_ip_address_for_device() -> str:
    """Returns the IP address for this device."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def _run_npm_build_commands() -> None:
    print("Installing react dependencies...")
    subprocess.run(["npm", "install"], check=True)
    print("Building react application...")
    subprocess.run(["npm", "run", "build"], check=True)


def _move_frontend_folder_to_backend(static_folder_name: str) -> None:
    print("moving build folder to backend...")
    target_path = os.path.join("./..", "backend", static_folder_name, "react")
    build_dir = _get_frontend_build_dir()
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.move(build_dir, target_path)


def _get_frontend_build_dir() -> str:
    for candidate in ("build", "dist"):
        if os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(
        "Frontend build output not found. Expected ./build or ./dist after npm run build."
    )
