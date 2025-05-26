# ship/task.py

import numpy as np

from loguru import logger
from gps_coordinate import (
    CircularGeofence,
    ObjectiveCoordinate,
    GPSPoint
)
from ship import (
    BlueLadyShipProperties,
    ShipState,
    ShipPosition
)


class ShipTaskManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ship_state: ShipState = None):
        self.ship_properties = BlueLadyShipProperties()

        if ship_state:
            self.ship_state = ship_state
        else:
            _geofence_center = GPSPoint(47.47, 19.03)  # ~ Kelenföld
            geofence = CircularGeofence(center=_geofence_center, radius_m=3_000)  # 3km
            starting_position = ShipPosition(geofence=geofence)
            self.ship_state = ShipState(starting_position)

        # Controller gains (from Table 5 in paper)
        self.k_psi_p = 1.6
        self.k_psi_d = 19.92
        self.k_y_p = 2.125
        self.k_y_i = 92.1

        self.y_error_integral = 0.0
        self.last_heading_error = 0.0

        # Control configuration
        self.constant_engine_rpm = 440  # default RPM from experiments

    def get_next_objective_coo(self) -> ObjectiveCoordinate:
        if len(self.ship_state.route) < 1:
            logger.warning(f"ShipState has no more objectives in route list!")
            return None

        return self.ship_state.route[0]

    def update_control(self) -> tuple[float, float]:
        segment = self.ship_state.current_segment
        if not segment:
            logger.warning("No active segment to compute control.")
            return 0.0, 0.0

        heading_error, cross_track_error = self._compute_errors(segment)
        rudder = self._compute_rudder(heading_error, cross_track_error)
        return rudder, self.constant_engine_rpm

    def _compute_errors(self, segment: tuple[GPSPoint, GPSPoint]) -> tuple[float, float]:
        position = self.ship_state.position
        wp_start, wp_end = segment

        cross_track = position.cross_track_error(segment)     # e_y
        _desired_heading = ShipPosition.compute_segment_course(wp_start, wp_end)
        heading_error = position.heading_error(_desired_heading)  # e_psi

        return heading_error, cross_track

    def _compute_rudder(self, heading_error: float, cross_track_error: float) -> float:
        # Derivative (Δe_ψ / Δt)
        heading_derivative = (heading_error - self.last_heading_error) / 0.2
        self.last_heading_error = heading_error

        # Integral ∫e_y dt
        self.y_error_integral += cross_track_error * 0.2

        # Control output (Eq. 45)
        rudder = (
            self.k_psi_p * heading_error +
            self.k_psi_d * heading_derivative +
            self.k_y_p * cross_track_error +
            self.k_y_i * self.y_error_integral
        )

        # Clamp to ±35° in radians
        return float(np.clip(rudder, np.radians(-35), np.radians(35)))
