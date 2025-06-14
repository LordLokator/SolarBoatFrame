# base.py

from threading import Lock
from math import radians, cos, sin, asin, sqrt
from loguru import logger
import warnings
import os

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    rotation="500 KB",
    backtrace=True,
    diagnose=True
)


class GPSPoint:
    def __init__(self, latitude: float, longitude: float):
        self._lock = Lock()
        self.latitude = latitude
        self.longitude = longitude

        msg = f"Initialized GPSPoint: ({self.latitude}, {self.longitude})"
        logger.debug(msg)

    def get_coordinates(self):
        with self._lock:
            return self.latitude, self.longitude

    def set_coordinates(self, coords: 'GPSPoint'):
        with self._lock:
            lat, lon = coords.get_coordinates()

            logger.debug(f"Setting coordinates from ({self.latitude}, {self.longitude}) to ({lat}, {lon})")
            self.latitude = lat
            self.longitude = lon

    def __set_coordinates(self, lat: float, lon: float):
        # This method is kept for emergencies.
        # Do not use it.
        # Setting these attributes manually is a crime against OOP.

        warnings.warn("This is a fallback method for setting coordinates. \
                      Use the more OOP 'set_coordinates' instead.", DeprecationWarning)

        with self._lock:
            msg = f"Setting coordinates from ({self.latitude}, {self.longitude}) to ({lat}, {lon})"
            logger.debug(msg)
            self.latitude = lat
            self.longitude = lon

    def haversine_distance(self, other: 'GPSPoint') -> float:
        """
        IDK hogy kell-e, de itt van.
        """

        logger.debug(f"Calculating distance from {self} to {other}")

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other.latitude)
        lon2 = radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        radius = 6371000  # Earth radius in meters
        distance = radius * c
        logger.debug(f"Calculated Haversine distance: {distance:.2f} meters")
        return distance

    def __repr__(self):
        return f"GPSPoint(lat={self.latitude}, lon={self.longitude})"
