import os
from typing import Optional
from pydantic import ValidationError
from .config import Config


def load_config(env_file: Optional[str] = ".env") -> Config:
    if env_file and not os.path.exists(env_file):
        raise FileNotFoundError(f"Env file not found at {env_file}.")
    try:
        return Config(_env_file=env_file)
    except ValidationError as exc:
        raise ValueError(f"Invalid config: {exc}") from exc
