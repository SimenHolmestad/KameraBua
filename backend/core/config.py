from typing import Optional, Dict, Any
import copy
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class WifiConfig(BaseModel):
    enabled: bool = False
    wifi_name: str = ""
    protocol: str = ""
    password: str = ""
    description: str = ""

    @model_validator(mode="after")
    def _validate_wifi_fields(self) -> "WifiConfig":
        if self.enabled:
            missing = [
                key for key, value in (
                    ("wifi_name", self.wifi_name),
                    ("protocol", self.protocol),
                    ("password", self.password),
                    ("description", self.description),
                )
                if not value
            ]
            if missing:
                raise ValueError(f"Missing wifi config fields: {', '.join(missing)}")
        return self


class QrCodeConfig(BaseModel):
    use_center_images: bool = True


DEFAULT_CAMERA_MODULES: Dict[str, Dict[str, Any]] = {
    "dummy": {
        "file_extension": ".png",
        "needs_raw_file_transfer": False,
        "raw_file_extension": None
    },
    "rpicam": {
        "file_extension": ".jpg",
        "needs_raw_file_transfer": False,
        "raw_file_extension": None
    },
    "dslr_jpg": {
        "file_extension": ".jpg",
        "needs_raw_file_transfer": False,
        "raw_file_extension": None
    },
    "dslr_raw": {
        "file_extension": ".jpg",
        "needs_raw_file_transfer": False,
        "raw_file_extension": None
    },
    "dslr_raw_transfer": {
        "file_extension": ".jpg",
        "needs_raw_file_transfer": True,
        "raw_file_extension": ".cr2"
    }
}


class CameraConfig(BaseModel):
    module: str = "dummy"
    options: Dict[str, Any] = Field(default_factory=dict)
    modules: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: copy.deepcopy(DEFAULT_CAMERA_MODULES)
    )


class AlbumConfig(BaseModel):
    forced_album: Optional[str] = None
    albums_dir: str

    @model_validator(mode="after")
    def _validate_albums_dir(self) -> "AlbumConfig":
        normalized_albums_dir = self.albums_dir.replace("\\", "/")
        if not normalized_albums_dir.startswith("backend/static/"):
            raise ValueError("albums_dir must start with 'backend/static/'")
        self.albums_dir = normalized_albums_dir
        return self


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CAMERAHUB_",
        env_nested_delimiter="__",
        extra="ignore",
    )
    static_folder_name: str = "static"
    albums: AlbumConfig = Field(default_factory=AlbumConfig)
    camera: CameraConfig = Field(default_factory=CameraConfig)
    qr_codes: QrCodeConfig = Field(default_factory=QrCodeConfig)
    wifi_qr_code: WifiConfig = Field(default_factory=WifiConfig)
