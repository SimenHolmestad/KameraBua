import os
from typing import Any, Dict, List, Optional
import qrcode
from PIL import Image
from backend.core.config import WifiConfig

QrCodeContext = Dict[str, Any]
QrCodeEntry = Dict[str, str]


def create_qr_code_context(static_dir_path: str, use_center_images: bool = False) -> QrCodeContext:
    qr_codes_dir_name = "qr_codes"
    qr_code_folder_path = os.path.join(static_dir_path, qr_codes_dir_name)
    os.makedirs(qr_code_folder_path, exist_ok=True)
    logo_image_path = None
    wifi_image_path = None

    if use_center_images:
        logo_image_path = _get_path_to_icon_file("Camera-icon.png")
        wifi_image_path = _get_path_to_icon_file("Wifi-icon.png")

    return {
        "qr_codes_dir_name": qr_codes_dir_name,
        "qr_code_folder_path": qr_code_folder_path,
        "qr_codes": [],
        "logo_image_path": logo_image_path,
        "wifi_image_path": wifi_image_path
    }


def add_url_qr_code(context: QrCodeContext, name: str, url: str, information_text: str) -> None:
    """Add a qr code containing a URL to the context."""
    _add_qr_code(
        context,
        name=name,
        content=url,
        information_text=information_text,
        center_image_path=context.get("logo_image_path")
    )


def add_wifi_qr_code(
    context: QrCodeContext,
    name: str,
    wifi_name: str,
    wifi_protocol: str,
    wifi_password: str,
    information_text: str
) -> None:
    """Add a qr code containing wifi information to the context."""
    wifi_qr_code_content = f"WIFI:S:{wifi_name};T:{wifi_protocol};P:{wifi_password};;"
    _add_qr_code(
        context,
        name=name,
        content=wifi_qr_code_content,
        information_text=information_text,
        center_image_path=context.get("wifi_image_path")
    )


def get_qr_codes(context: QrCodeContext) -> List[QrCodeEntry]:
    return context.get("qr_codes", [])


def get_qr_code_urls_as_strings(context: QrCodeContext, host_ip: str) -> List[str]:
    return [
        f"For accessing {qr_code['name']} : {_get_absolute_url_for_qr_code(qr_code, host_ip)}"
        for qr_code in get_qr_codes(context)
    ]


def create_qr_codes_with_config(
    static_folder_path: str,
    host_ip: str,
    port: int,
    use_center_images: bool = False,
    forced_album_name: Optional[str] = None,
    wifi_config: Optional[WifiConfig] = None
) -> QrCodeContext:
    context = create_qr_code_context(static_folder_path, use_center_images)
    _add_wifi_qr_code_from_config(context, wifi_config)

    start_page_url = get_start_page_url(host_ip, port, forced_album_name)
    add_url_qr_code(
        context,
        "start_page_url",
        start_page_url,
        "Scan this qr code to go to CameraHub!"
    )
    return context


def get_start_page_url(host_ip: str, port: int, forced_album_name: Optional[str] = None) -> str:
    if forced_album_name:
        return f"http://{host_ip}:{port}/album/{forced_album_name}"
    return f"http://{host_ip}:{port}/"


def _add_qr_code(
    context: QrCodeContext,
    name: str,
    content: str,
    information_text: str,
    center_image_path: Optional[str]
) -> None:
    filename = name + ".png"
    qr_code_file_path = os.path.join(context["qr_code_folder_path"], filename)
    _generate_qr_code(qr_code_file_path, content, center_image_path)
    context["qr_codes"].append({
        "name": name,
        "information": information_text,
        "relative_url": f"{context['qr_codes_dir_name']}/{filename}"
    })


def _generate_qr_code(
    qr_code_file_path: str,
    content: str,
    center_image_path: Optional[str] = None,
    qr_image_size: int = 1024,
    center_image_size: int = 256
) -> None:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((1024, 1024))

    if center_image_path:
        qr_img = _paste_image_in_center(qr_img, center_image_path, qr_image_size, center_image_size)

    qr_img.save(qr_code_file_path)


def _paste_image_in_center(
    background: Image.Image,
    center_image_path: str,
    qr_image_size: int,
    center_image_size: int
) -> Image.Image:
    paste_img = Image.open(center_image_path, 'r').convert("RGBA").resize((center_image_size, center_image_size))
    offset_value = (qr_image_size - center_image_size) // 2
    offset = ((offset_value, offset_value))
    background.paste(paste_img, offset, paste_img)
    return background


def _get_absolute_url_for_qr_code(qr_code: QrCodeEntry, host_ip: str) -> str:
    return "http://" + host_ip + ":5000/static/" + qr_code["relative_url"]


def _add_wifi_qr_code_from_config(context: QrCodeContext, wifi_config: Optional[WifiConfig]) -> None:
    if isinstance(wifi_config, WifiConfig) and wifi_config.enabled:
        add_wifi_qr_code(
            context,
            "wifi_qr_code",
            wifi_config.wifi_name,
            wifi_config.protocol,
            wifi_config.password,
            wifi_config.description
        )


def _get_path_to_icon_file(filename: str) -> str:
    return os.path.join(
        "scripts",
        "assets",
        "qr_codes",
        "icons",
        filename
    )
