from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator


class WifiSettings(BaseModel):
    enabled: bool = True
    name: str = ""
    protocol: str = ""
    password: str = ""
    description: str = ""

    @model_validator(mode="after")
    def _validate_wifi_fields(self) -> "WifiSettings":
        if self.enabled:
            missing = [
                key for key, value in (
                    ("name", self.name),
                    ("protocol", self.protocol),
                    ("password", self.password),
                    ("description", self.description),
                )
                if not value
            ]
            if missing:
                raise ValueError("Missing wifi config fields: {}".format(", ".join(missing)))
        return self


class QrCodeSettings(BaseModel):
    use_center_images: bool = True
    wifi: WifiSettings = Field(default_factory=WifiSettings)


class CameraSettings(BaseModel):
    module: str = "dummy"
    options: Dict[str, Any] = Field(default_factory=dict)


class AlbumSettings(BaseModel):
    forced_album: Optional[str] = None


class Settings(BaseModel):
    albums: AlbumSettings = Field(default_factory=AlbumSettings)
    camera: CameraSettings = Field(default_factory=CameraSettings)
    qr_codes: QrCodeSettings = Field(default_factory=QrCodeSettings)
