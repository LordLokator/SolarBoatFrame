# buoy.py

import os
from .base import GPSPoint
from loguru import logger

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    rotation="500 KB",
    backtrace=True,
    diagnose=True
)


class BuoyPosition(GPSPoint):
    """
    Represents a static buoy with a radius (in meters).
    """

    def __init__(self, latitude: float, longitude: float, radius: float):
        super().__init__(latitude, longitude)
        self.radius = radius

        msg = f"Initialized BuoyPosition at ({self.latitude}, {self.longitude}) with radius {self.radius}m"
        logger.debug(msg)

    def is_within_radius(self, point: GPSPoint) -> bool:
        distance = self.haversine_distance(point)
        result = distance <= self.radius

        msg = f"Checking if point {point} is within {self.radius}m of buoy: {result}"
        logger.debug(msg)
        return result
