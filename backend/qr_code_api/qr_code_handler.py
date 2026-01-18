import os
from typing import List, Optional
from backend.album_storage.folder import Folder
from backend.settings import WifiSettings
from .qr_code import QrCode


class QrCodeHandler:
    """A class for creating an keeping track of qr-codes and related
    information.
    """

    def __init__(self, static_dir_path: str, use_center_images: bool = False) -> None:
        self.qr_code_folder = Folder(static_dir_path, "qr_codes")
        self.qr_codes = []
        self.logo_image_path = None
        self.wifi_image_path = None

        if use_center_images:
            self.logo_image_path = self.__get_path_to_icon_file("Camera-icon.png")
            self.wifi_image_path = self.__get_path_to_icon_file("Wifi-icon.png")

    def add_url_qr_code(self, name: str, url: str, information_text: str) -> None:
        """Add a qr_code containing and url to the qr code handler"""
        self.qr_codes.append(
            QrCode(
                self.qr_code_folder,
                name,
                url,
                information_text,
                self.logo_image_path
            )
        )

    def add_wifi_qr_code(
        self,
        name: str,
        wifi_name: str,
        wifi_protocol: str,
        wifi_password: str,
        information_text: str
    ) -> None:
        """Add a qr_code containing and wifi information to the qr code handler"""
        wifi_qr_code_content = F"WIFI:S:{wifi_name};T:{wifi_protocol};P:{wifi_password};;"
        self.qr_codes.append(
            QrCode(
                self.qr_code_folder,
                name,
                wifi_qr_code_content,
                information_text,
                self.wifi_image_path
            )
        )

    def get_qr_codes(self) -> List[QrCode]:
        return self.qr_codes

    def get_qr_code_urls_as_strings(self, host_ip: str) -> List[str]:
        return list(map(
            lambda qr_code:
            "For accessing "
            + qr_code.get_name()
            + " : "
            + self.__get_absolute_url_for_qr_code(qr_code, host_ip),
            self.get_qr_codes()
        ))

    def __get_absolute_url_for_qr_code(self, qr_code: QrCode, host_ip: str) -> str:
        return "http://" + host_ip + ":5000/static/" + qr_code.get_relative_url()

    def create_qr_code_handler_with_qr_codes(
        static_folder_path: str,
        host_ip: str,
        port: int,
        use_center_images: bool = False,
        forced_album_name: Optional[str] = None,
        wifi_settings: Optional[WifiSettings] = None
    ) -> "QrCodeHandler":
        qr_code_handler = QrCodeHandler(static_folder_path, use_center_images)
        qr_code_handler.__add_wifi_qr_code_from_settings(wifi_settings)

        start_page_url = QrCodeHandler.get_start_page_url(host_ip, port, forced_album_name)
        qr_code_handler.add_url_qr_code(
            "start_page_url",
            start_page_url,
            "Scan this qr code to go to CameraHub!"
        )
        return qr_code_handler

    def get_start_page_url(host_ip: str, port: int, forced_album_name: Optional[str] = None) -> str:
        if forced_album_name:
            return "http://{}:{}/album/{}".format(host_ip, port, forced_album_name)
        return "http://{}:{}/".format(host_ip, port)

    def __add_wifi_qr_code_from_settings(self, wifi_settings: Optional[WifiSettings]) -> None:
        if isinstance(wifi_settings, WifiSettings) and wifi_settings.enabled:
            self.add_wifi_qr_code(
                "wifi_qr_code",
                wifi_settings.name,
                wifi_settings.protocol,
                wifi_settings.password,
                wifi_settings.description
            )

    def __get_path_to_icon_file(self, filename: str) -> str:
        return os.path.join(
            "assets",
            "image_resources",
            "icons",
            filename
        )
