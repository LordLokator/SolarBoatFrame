# ship/ship_state.py
"""Ide kellenek a dinamikus tulajdonságok."""

from loguru import logger
import numpy as np
from gps_coordinate import (
    ObjectiveCoordinate,
    GPSPoint
)

from . import ShipPosition, BlueLadyShipProperties


class ShipState:
    """Manages the dynamic properties of the ship, like current position"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, starting_position: ShipPosition):
        self.position: ShipPosition = starting_position
        self.route: list[ObjectiveCoordinate] = []  # init?
        self.current_segment_index = 0  # so we can keep the route list

        self.properties = BlueLadyShipProperties()  # change for Lana!

        # CAN-fed dynamic state
        # NOTE: Other CAN variables can be added here later
        self.engine_rpm: float = 0.0
        self.rudder_angle: float = 0.0

    # region Properties

    @property
    def current_segment(self) -> tuple[GPSPoint, GPSPoint]:
        try:
            return (self.route[self.current_segment_index],
                    self.route[self.current_segment_index + 1])
        except IndexError:
            logger.warning("No next segment available")
            return None

    # endregion

    def advance_to_next_segment(self):
        if self.current_segment_index + 2 <= len(self.route):
            self.current_segment_index += 1
            logger.info(f"Advanced to segment {self.current_segment_index}")
        else:
            logger.info("Final segment reached")


    def update_from_can(self, u: float, v: float, r: float, rudder_angle: float, engine_rpm: float):
        # Use this function when the CANManager reads new data
        self.position.u = u
        self.position.v = v
        self.position.r = r
        self.rudder_angle = rudder_angle
        self.engine_rpm = engine_rpm

    def eta_dot(self) -> np.ndarray:
        """Calculate Earth-frame velocity \u03b7_dot = R(psi) * nu (Equation 2)."""
        R = self.rotation_matrix()
        return R @ self.position.nu

    def rotation_matrix(self) -> np.ndarray:
        """Return the rotation matrix R(psi) from body to Earth frame (Equation 3)."""

        _psi = self.position.heading_psi
        c = np.cos(_psi)
        s = np.sin(_psi)

        return np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])
