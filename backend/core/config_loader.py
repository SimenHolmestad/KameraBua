import json
import os
from typing import Any, Dict
from pydantic import ValidationError
from .config import Config


def load_config(config_path: str = os.path.join("configs", "config.json")) -> Config:
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Config file not found at {config_path}. Create it based on configs/example_config.json."
        )
    with open(config_path, "r") as f:
        raw: Dict[str, Any] = json.loads(f.read())

    try:
        return Config.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Invalid config: {exc}") from exc
