# ship_state/ship_state.py
"""Ide kellenek a dinamikus tulajdonságok."""

from loguru import logger
import numpy as np
from gps_coordinate import ObjectiveCoordinate, ShipPosition
from .ship_properties import BlueLadyShipProperties


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
        self.properties = BlueLadyShipProperties()

        self.psi: float  # heading in radians (w.r.t North)
        self.u: float  # surge speed
        self.v: float  # sway speed
        self.r: float  # yaw rate

    @property
    def Xn(self):
        Xn = self.current_position.Xn
        if Xn is None or not isinstance(Xn, float):
            err_msg = f"Xn is supposed to be of type float, it is instead [{type(Xn)}] with value [{Xn}]!"
            logger.critical(err_msg)
            raise ValueError(err_msg)

        return Xn

    @property
    def Yn(self):
        Yn = self.current_position.Yn
        if Yn is None or not isinstance(Yn, float):
            err_msg = f"Yn is supposed to be of type float, it is instead [{type(Yn)}] with value [{Yn}]!"
            logger.critical(err_msg)
            raise ValueError(err_msg)

        return Yn

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
