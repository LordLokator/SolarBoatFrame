# ship_state/ship_state.py
"""Ide kellenek a dinamikus tulajdonságok."""

import numpy as np
from gps_coordinate import ObjectiveCoordinate, ShipPosition
from .ship_properties import ShipProperties


class ShipState:
    """Manages the dynamic properties of the ship, like current position
    """

    _instance = None

    def __new__(cls, starting_position):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, starting_position: ShipPosition):
        self.current_position: ShipPosition = starting_position
        self.route: list[ObjectiveCoordinate] = []  # init?
        self.properties = ShipProperties()

        self.x: float  # Earth-fixed x
        self.y: float  # Earth-fixed y
        self.psi: float  # heading in radians (w.r.t North)
        self.u: float  # surge speed
        self.v: float  # sway speed
        self.r: float  # yaw rate

    def eta(self) -> np.ndarray:
        """Return position and heading vector in Earth-fixed frame."""
        return np.array([self.x, self.y, self.psi])

    def nu(self) -> np.ndarray:
        """Return velocity vector in Body-fixed frame."""
        return np.array([self.u, self.v, self.r])

    def x_state(self) -> np.ndarray:
        """Full state vector x = [eta.T, nu.T].T"""
        return np.concatenate((self.eta(), self.nu()))

    def eta_dot(self) -> np.ndarray:
        """Calculate Earth-frame velocity \u03b7_dot = R(psi) * nu (Equation 2)."""
        R = self.rotation_matrix()
        nu = self.nu()
        return R @ nu

    def rotation_matrix(self) -> np.ndarray:
        """Return the rotation matrix R(psi) from body to Earth frame (Equation 3)."""

        c = np.cos(self.psi)
        s = np.sin(self.psi)

        return np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])

        # TODO
        ...
