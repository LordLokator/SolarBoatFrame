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

    # endregion

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

    def get_body_referenced_coordinates(self, reference) -> tuple[float, float]:
        Xb, Yb = self.position._get_body_referenced_coordinates(
            reference=reference,
            heading_psi=self.psi
        )
        return (Xb, Yb)

    # TODO
    ...
