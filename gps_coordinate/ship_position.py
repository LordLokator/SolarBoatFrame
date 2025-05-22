# ship_position.py

from math import sin, cos
import os
from threading import Lock
from loguru import logger

from .geofence import CircularGeofence, PolygonalGeofence
from .objective import ObjectiveCoordinate
from .base import GPSPoint

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    backtrace=True,
    diagnose=True
)


class ShipPosition(GPSPoint):
    _instance = None
    _singleton_lock = Lock()
    _lock = Lock()

    def __new__(cls, latitude=0.0, longitude=0.0, geofence=None):
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

    # region properties

    # endregion

    def _get_body_referenced_coordinates(self, reference: GPSPoint, heading_psi: float) -> tuple[float, float]:
        """Returns a body-referenced coordinate pair of (Xb, Yb).

        Args:
            reference (GPSPoint): Reference point.

        Returns:
            tuple[float, float]: (Xb, Yb)
        """
        north, east = self.ned_offset(reference)

        Xb = cos(heading_psi) * north + sin(heading_psi) * east
        Yb = -sin(heading_psi) * north + cos(heading_psi) * east
        return (Xb, Yb)

    def ned_offset(self, reference_point: GPSPoint) -> tuple[float, float]:
        """
        NED offset relative to a fixed Earth frame origin.
        For body-frame projection, the origin is the initial position.
        """
        if reference_point is None:
            logger.warning("Origin not set for body-fixed transformation. Using self.")
            reference_point = self
        return self.ned_offset_from(reference_point)

    def update_position(self, new_objective: ObjectiveCoordinate) -> bool:

        if not self.geofence.contains(new_objective):
            logger.warning("Attempted to move outside geofence!")
            return False

        else:
            self.set_coordinates(new_objective)
            return True

    def is_within_geofence(self) -> bool:
        ship_in_geofence = self.geofence.contains(self)
        return ship_in_geofence
