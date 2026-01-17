import os
import shutil
import socket
import platform
import subprocess
from abc import ABC, abstractmethod
from backend.qr_code_api.qr_code_handler import QrCodeHandler
from backend.camera_module_options import get_instance_of_camera_module_by_name
from backend.album_storage.folder_album_handler import FolderAlbumHandler


class BaseRunConfig(ABC):
    """Abstract class containing common function for doing some app
    function.
    """

    def __init__(self,
                 args,
                 raw_args,
                 static_folder_name="static",
                 debug_port=3000,
                 production_port=5000):
        self.args = args
        self.raw_args = raw_args
        self.static_folder_name = static_folder_name
        self.static_folder_path = os.path.join("backend", static_folder_name)
        self.debug_port = debug_port
        self.production_port = production_port
        self.host_ip = self.__find_ip_address_for_device()

    @abstractmethod
    def run(self):
        pass

    def build_frontend(self):
        os.chdir("frontend")
        self.__run_npm_build_commands()
        self.__move_frontend_folder_to_flask()
        os.chdir("./..")

    def frontend_is_built(self):
        node_modules_path = os.path.join(
            "frontend",
            "node_modules"
        )
        build_folder_path = os.path.join(
            "backend",
            "static",
            "react"
        )
        return os.path.exists(node_modules_path) and os.path.exists(build_folder_path)

    def open_webpage_in_device_browser(self, url):
        """If chromium is used, the chromium subprocess is returned so that
        it can be terminated later.
        """
        if(os.path.exists("/usr/bin/chromium-browser")):
            os.environ["DISPLAY"] = ":0"
            cmd = ["sleep", "2", "&&" "/usr/bin/chromium-browser", "--start-fullscreen", url]
            # Return a chromium subprocessed with suppressed output
            with open(os.devnull, 'w') as fp:
                return subprocess.Popen(" ".join(cmd), shell=True, stdout=fp, stderr=fp)
        elif platform.system() == "Darwin":
            cmd = "open " + url
            subprocess.run(cmd, shell=True)

        return None

    def create_qr_code_handler(self, port):
        return QrCodeHandler.create_qr_code_handler_with_qr_codes(
            self.static_folder_path,
            self.host_ip,
            port,
            use_center_images=True,
            forced_album_name=self.args.force_album
        )

    def get_url_for_qr_code_page(self, port):
        if self.args.force_album:
            return "http://{}:{}/album/{}/last_image_qr".format(
                self.host_ip,
                str(port),
                self.args.force_album
            )
        return "http://{}:{}/qr".format(self.host_ip, str(port))

    def get_camera_module_instance(self):
        return get_instance_of_camera_module_by_name(self.args.camera_module)

    def get_album_handler_instance(self):
        return FolderAlbumHandler(self.static_folder_path, "albums")

    def ensure_forced_album_is_created(self, album_handler):
        if self.args.force_album:
            album_handler.get_or_create_album(self.args.force_album)

    def __find_ip_address_for_device(self):
        """Returns the IP address for this device"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def __run_npm_build_commands(self):
        with open(os.devnull, 'w') as fp:
            print("Installing react dependencies...")
            subprocess.run("npm install", shell=True, stdout=fp)
            print("Building react application...")
            subprocess.run("npm run build", shell=True, stdout=fp)

    def __move_frontend_folder_to_flask(self):
        print("moving build folder to flask...")
        if os.path.exists("./../backend/static/react"):
            shutil.rmtree("./../backend/static/react")
        shutil.move("./build", "./../backend/static/react")
