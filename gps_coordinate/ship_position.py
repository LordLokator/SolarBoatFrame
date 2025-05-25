# ship_position.py

from math import sin, cos
import os
from threading import Lock
import threading
import time
from loguru import logger

from managers import GPSManager

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

UPDATE_INTERVAL = 0.1  # 1/10 second


class ShipPosition(GPSPoint):
    _instance = None
    _singleton_lock = Lock()
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, geofence: CircularGeofence | PolygonalGeofence = None, gps_manager: GPSManager = None):
        if self._initialized:
            return

        self._initialized = True

        # Ha nem létezik a '__initialized' attributum, hamisnak vesszük;
        if not getattr(self, '__initialized', False):

            self._gps = self._gps = gps_manager if gps_manager else GPSManager()

            latitude, longitude = self._gps.get_live_location()

            if latitude is None or longitude is None:
                msg = f"ShipPosition couldn't get live GPS and didn't recieve valid initial lat-lon!"
                logger.error(msg)
                raise ValueError(msg)

            super().__init__(latitude, longitude)

            # '"__initialized" is not accessed - Pylance' ->
            # A 'getattr' igenis eléri, csak ezt a linter nem tudja szegény
            self.__initialized = True
            self.geofence = geofence
            self._running = False
            self._thread: threading.Thread = None

    # region properties

    # endregion

    def _update_loop(self):
        while self._running:
            lat, lon = self._gps.get_live_location()
            if lat is not None and lon is not None:
                with self._lock:
                    self.latitude = lat
                    self.longitude = lon
                    logger.debug("ShipPosition updated: lat={}, lon={}", lat, lon)
            time.sleep(UPDATE_INTERVAL)

    def start_auto_update(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._update_loop, daemon=True)
            self._thread.start()
            logger.info("Auto-update thread started.")

    def stop_auto_update(self):
        if self._running:
            self._running = False
            self._thread.join()
            logger.info("Auto-update thread stopped.")

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
