from typing import Optional
from random import randint
import matplotlib.pyplot as plt
import numpy as np
from .base_camera_module import BaseCameraModule


class DummyCameraModule(BaseCameraModule):
    """Dummy camera module for creating somewhat random images without a
    camera"""

    def __init__(self,
                 file_extension: str = ".png",
                 width: int = 1200,
                 height: int = 800,
                 number_of_circles: int = 80,
                 min_circle_radius: int = 30,
                 max_circle_radius: int = 80) -> None:
        super().__init__(file_extension)
        self.width = width
        self.height = height
        self.number_of_circles = number_of_circles
        self.min_circle_radius = min_circle_radius
        self.max_circle_radius = max_circle_radius

    def add_random_circle_to_image(self, image: np.ndarray) -> np.ndarray:
        """Add a random circle to the image based on the input parameters of
        the class. The function returns the input image with the added
        circle."""
        x_center = randint(0, self.width - 1)
        y_center = randint(0, self.height - 1)
        radius = randint(self.min_circle_radius, self.max_circle_radius)
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        # Create start and endpoints as iterating through the whole
        # image is not necessary
        x_start = max(0, x_center - radius - 1)
        x_end = min(self.width, x_center + radius + 1)
        y_start = max(0, y_center - radius - 1)
        y_end = min(self.height, y_center + radius + 1)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if (x - x_center)**2 + (y - y_center)**2 < radius**2:
                    image[y, x, 0] = r
                    image[y, x, 1] = g
                    image[y, x, 2] = b
        return image

    def capture_image(self, image_path: str, raw_file_path: Optional[str] = None) -> None:
        """Creates an image and saves it in "image_path"."""
        # Create white image
        image = np.full((self.height, self.width, 3), 255, dtype=np.uint8)

        # Add circles to image
        for x in range(self.number_of_circles):
            image = self.add_random_circle_to_image(image)

        # Save image
        plt.imsave(image_path, image)
