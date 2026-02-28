from random import randint
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from backend.core.config import DummyCameraConfig
from .errors import ImageCaptureError


def create_dummy_image(config: DummyCameraConfig, base_image_path: str) -> None:
    if config.should_fail:
        raise ImageCaptureError(config.error_message)

    image_path = base_image_path + ".png"
    image = np.full((config.height, config.width, 3), 255, dtype=np.uint8)
    for _ in range(config.number_of_circles):
        image = _add_random_circle_to_image(
            image,
            config.width,
            config.height,
            config.min_circle_radius,
            config.max_circle_radius,
            randint
        )
    plt.imsave(image_path, image)


def _add_random_circle_to_image(
    image: Any,
    width: int,
    height: int,
    min_circle_radius: int,
    max_circle_radius: int,
    randint_fn: Any
) -> Any:
    x_center = randint_fn(0, width - 1)
    y_center = randint_fn(0, height - 1)
    radius = randint_fn(min_circle_radius, max_circle_radius)
    r = randint_fn(0, 255)
    g = randint_fn(0, 255)
    b = randint_fn(0, 255)

    x_start = max(0, x_center - radius - 1)
    x_end = min(width, x_center + radius + 1)
    y_start = max(0, y_center - radius - 1)
    y_end = min(height, y_center + radius + 1)

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            if (x - x_center) ** 2 + (y - y_center) ** 2 < radius ** 2:
                image[y, x, 0] = r
                image[y, x, 1] = g
                image[y, x, 2] = b
    return image
