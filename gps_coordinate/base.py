# base.py

from pyproj import Transformer
from threading import Lock
from math import radians, cos, sin, asin, sqrt
from loguru import logger
import warnings
import os

from .config import (
    WGS84_GPS,
    EPSG_32634_BP,
    EPSG_32633_BALATON,
    EPSG_32632_MONACO
)

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    backtrace=True,
    diagnose=True
)


class GPSPoint:

    _TRANSFORMER: Transformer = None
    # _TRANSFORMER = Transformer.from_crs(WGS84_GPS, EPSG_32633_BALATON, always_xy=True)
    # _TRANSFORMER_2_WGS = Transformer.from_crs(EPSG_32633_BALATON, WGS84_GPS, always_xy=True)

    def __init__(self, latitude: float, longitude: float, cs_from=WGS84_GPS, crs_to=EPSG_32634_BP):

        self._TRANSFORMER = Transformer.from_crs(cs_from, crs_to, always_xy=True)
        self.transformer_target_name: str = ({
            "EPSG_32634_BP": EPSG_32634_BP,
            "EPSG_32633_BALATON": EPSG_32633_BALATON,
            "EPSG_32632_MONACO": EPSG_32632_MONACO,
            "WGS84_GPS": WGS84_GPS,
        }).get(crs_to, "Unknown CRS type.")

        self._lock = Lock()
        self.latitude = latitude
        self.longitude = longitude

        # if not str(EPSG_32634_BP).endswith(str(self._utm_zone())):
        #     logger.warning(f"UTM Zone mismatch! Calculated: [{self._utm_zone()}] | Used: [{EPSG_32634_BP}]")

        msg = f"Initialized GPSPoint: ({self.latitude}, {self.longitude})"
        logger.debug(msg)

    @property
    def Xn(self) -> float:
        x, _ = self._TRANSFORMER.transform(self.longitude, self.latitude)
        return x

    @property
    def Yn(self) -> float:
        _, y = self._TRANSFORMER.transform(self.longitude, self.latitude)
        return y

    def set_from_Xn_Yn(self, x: float, y: float) -> None:
        """Set GPSPoint using projected coordinates (Xn, Yn)"""
        lon, lat = self._TRANSFORMER.transform(x, y, direction='INVERSE')
        with self._lock:
            logger.debug(f"Setting from XY=({x:.2f}, {y:.2f}) → latlon=({lat:.6f}, {lon:.6f})")
            self.latitude = lat
            self.longitude = lon


    def _utm_zone(self):
        return int((self.longitude + 180) / 6) + 1

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

    def ned_offset_from(self, origin: 'GPSPoint') -> tuple[float, float]:
        with self._lock:
            north = self.Yn - origin.Yn
            east = self.Xn - origin.Xn
            return north, east

    def __repr__(self) -> str:
        return f"GPSPoint(lat={self.latitude}, lon={self.longitude})"
