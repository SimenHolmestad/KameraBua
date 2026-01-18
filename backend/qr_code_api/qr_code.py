from typing import Optional
import qrcode
from PIL import Image
from backend.album_storage.folder import Folder


class QrCode:
    """A class for creating an keeping track of a single qr code. If
    center_image_path is specified, the image in the path will be
    added to the center of the qr-code. Keep in mind that these center
    images needs to be square.

    """

    def __init__(self,
                 qr_code_folder: Folder,
                 name: str,
                 content: str,
                 information_text: str,
                 center_image_path: Optional[str] = None,
                 qr_image_size: int = 1024,
                 center_image_size: int = 256) -> None:
        self.folder: Folder = qr_code_folder
        self.name: str = name
        self.filename: str = self.name + ".png"
        self.information_text: str = information_text
        self.center_image_path: Optional[str] = center_image_path
        self.qr_image_size: int = qr_image_size
        self.center_image_size: int = center_image_size
        self.__generate_qr_code(self.folder.get_path_to_file(self.filename), content)

    def get_relative_url(self) -> str:
        return "{}/{}".format(
            self.folder.get_name(),
            self.filename
        )

    def get_name(self) -> str:
        return self.name

    def get_information_text(self) -> str:
        return self.information_text

    def __generate_qr_code(self, qr_code_file_path: str, content: str) -> None:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(content)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((1024, 1024))

        if self.center_image_path:
            qr_img = self.__paste_image_in_center(qr_img, self.center_image_path)

        qr_img.save(qr_code_file_path)

    def __paste_image_in_center(self, background: Image.Image, center_image_path: str) -> Image.Image:
        paste_img = Image.open(center_image_path, 'r').convert("RGBA").resize((256, 256))
        offset_value = (self.qr_image_size - self.center_image_size) // 2
        offset = ((offset_value, offset_value))
        background.paste(paste_img, offset, paste_img)
        return background
