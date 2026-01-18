import json
import os
from typing import Any, Dict
from pydantic import ValidationError
from .settings import Settings


def load_settings(config_path: str = os.path.join("config", "config.json")) -> Settings:
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "Config file not found at {}. Create it based on the example schema.".format(config_path)
        )
    with open(config_path, "r") as f:
        raw: Dict[str, Any] = json.loads(f.read())

    try:
        return Settings.model_validate(raw)
    except ValidationError as exc:
        raise ValueError("Invalid config: {}".format(exc)) from exc
