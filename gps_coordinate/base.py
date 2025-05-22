# base.py

from pyproj import Transformer, CRS
from threading import Lock
from math import radians, cos, sin, asin, sqrt
from loguru import logger
import warnings
import os

from .config import WGS84_GPS, EPSG_32634_BP

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    backtrace=True,
    diagnose=True
)


class GPSPoint:

    _CRS_GEODETIC = CRS.from_epsg(WGS84_GPS)
    _CRS_PROJECTED = CRS.from_epsg(EPSG_32634_BP)
    _TRANSFORMER = Transformer.from_crs(_CRS_GEODETIC, _CRS_PROJECTED, always_xy=True)

    def __init__(self, latitude: float, longitude: float):
        self._lock = Lock()
        self.latitude = latitude
        self.longitude = longitude
        self.Xn: float = None
        self.Yn: float = None

        self.update_projected_coordinates()

        msg = f"Initialized GPSPoint: ({self.latitude}, {self.longitude})"
        logger.debug(msg)

    # def _utm_zone(self):
    #     return int((self.longitude + 180) / 6) + 1

    def update_projected_coordinates(self) -> None:
        with self._lock:
            self.Xn, self.Yn = self._TRANSFORMER.transform(self.longitude, self.latitude)
            logger.debug(f"Updated projected coordinates: Xn={self.Xn:.2f}, Yn={self.Yn:.2f}")

    def get_coordinates(self) -> tuple[float, float]:
        with self._lock:
            return self.latitude, self.longitude

    def set_coordinates(self, coords: 'GPSPoint') -> None:
        with self._lock:
            lat, lon = coords.get_coordinates()

            logger.debug(f"Setting coordinates from ({self.latitude}, {self.longitude}) to ({lat}, {lon})")
            self.latitude = lat
            self.longitude = lon

    def __set_coordinates(self, lat: float, lon: float) -> None:
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

    def __repr__(self) -> str:
        return f"GPSPoint(lat={self.latitude}, lon={self.longitude})"
