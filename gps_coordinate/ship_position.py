# ship_position.py

import os
from threading import Lock
from loguru import logger

from gps_coordinate.geofence import CircularGeofence, PolygonalGeofence
from gps_coordinate.objective import ObjectiveCoordinate
from .base import GPSPoint

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    rotation="500 KB",
    backtrace=True,
    diagnose=True
)


class ShipPosition(GPSPoint):
    _instance = None
    _singleton_lock = Lock()
    _lock = Lock()

    def __new__(cls, latitude=0.0, longitude=0.0):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, latitude=0.0, longitude=0.0, geofence: CircularGeofence | PolygonalGeofence = None):

        # Ha nem létezik a '__initialized' attributum, hamisnak vesszük;
        if not getattr(self, '__initialized', False):
            super().__init__(latitude, longitude)

            # '"__initialized" is not accessed - Pylance' ->
            # A 'getattr' igenis eléri, csak ezt a linter nem tudja szegény
            self.__initialized = True
            self.geofence = geofence

    def update_position(self, new_objective: ObjectiveCoordinate):

        if not self.geofence.contains(self.get_coordinates()):
            logger.warning("Attempted to move outside geofence!")
            return

        self.set_coordinates(new_objective)

    def is_within_geofence(self) -> bool:
        ship_in_geofence = self.geofence.contains(self.get_coordinates())
        return ship_in_geofence
