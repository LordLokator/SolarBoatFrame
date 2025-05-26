# ship/ship_position.py

from math import sin, cos
import os
from threading import Lock
import threading
import time
from typing import Optional
from loguru import logger

from managers import GPSManager

from gps_coordinate import (
    GPSPoint,
    CircularGeofence,
    PolygonalGeofence
)

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


        self._gps = self._gps = gps_manager if gps_manager else GPSManager()

        latitude, longitude = self._gps.get_live_location()

        if latitude is None or longitude is None:
            msg = f"ShipPosition couldn't get live GPS and didn't recieve valid initial lat-lon!"
            logger.error(msg)
            raise ValueError(msg)

        super().__init__(latitude, longitude)

        self.geofence = geofence
        self._running = False
        self._thread: threading.Thread = None

        self.reference_point: GPSPoint = GPSPoint(
            self.latitude,
            self.longitude
        )

        self._heading_psi: float = 0.0  # heading in radians (w.r.t North)
        self.u: float = 0.0  # surge speed
        self.v: float = 0.0  # sway speed
        self.r: float = 0.0  # yaw rate

    # region properties

    @property
    def heading_psi(self) -> Optional[float]:
        """Current heading angle in radians (from North, right-handed)."""
        with self._lock:
            return self._heading_psi

    @heading_psi.setter
    def heading_psi(self, value_rad: float):
        """Sets the heading angle and logs the access."""
        with self._lock:
            self._heading_psi = value_rad
            logger.debug("Heading angle (ψ) updated to {:.3f} rad", value_rad)

    @property
    def XnYn_earth(self) -> tuple[float, float]:
        Xn = self.Xn
        Yn = self.Yn

        if Xn is None or not isinstance(Xn, float) or \
           Yn is None or not isinstance(Yn, float):
            err_msg = f"XnYn is supposed to be of type float, it is instead \
                [{type(Xn)}-{type(Yn)}] with value [{Xn}-{Yn}]!"

            logger.critical(err_msg)
            raise ValueError(err_msg)

        return (Xn, Yn)

    @property
    def XbYb_body(self) -> tuple[float, float]:
        """
        Returns current (Xb, Yb) coordinates relative to the ship's reference
        frame. Requires self.heading_psi and self.reference_point to be set.

        Returns:
            tuple[float, float]: (Xb, Yb)
        """

        if self.reference_point is None or self.heading_psi is None:
            raise ValueError("Reference point and heading must be set.")

        north, east = self.ned_offset(self.reference_point)

        cos_psi = cos(self.heading_psi)
        sin_psi = sin(self.heading_psi)

        Xb = cos_psi * north + sin_psi * east
        Yb = -sin_psi * north + cos_psi * east

        return (Xb, Yb)

    # endregion

    def update_position_with_gps_data(self):
        lat, lon = self._gps.get_live_location()
        if lat is not None and lon is not None:
            self.set_ship_position(GPSPoint(lat, lon))

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

    def set_ship_position(self, position: GPSPoint) -> bool:
        """Sets the ship's position to the given coordinates if they are within the geofence.

        Args:
            position (GPSPoint): Target coordinates.

        Returns:
            bool: Success.
        """
        if not self.geofence.contains(position):
            logger.warning("Attempted to move outside geofence!")
            return False

        else:
            self.set_coordinates(position)
            return True

    def is_within_geofence(self) -> bool:
        ship_in_geofence = self.geofence.contains(self)
        return ship_in_geofence
