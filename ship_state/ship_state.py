# ship_state/ship_state.py
"""Ide kellenek a dinamikus tulajdonságok."""

from loguru import logger
import numpy as np
from gps_coordinate import ObjectiveCoordinate, ShipPosition
from gps_coordinate import GPSPoint
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
        self.position: ShipPosition = starting_position
        self.origin_position: GPSPoint = GPSPoint(self.position.latitude, self.position.longitude)
        self.route: list[ObjectiveCoordinate] = []  # init?
        self.properties = BlueLadyShipProperties()

        self.psi: float = 0.0  # heading in radians (w.r.t North)
        self.u: float = 0.0  # surge speed
        self.v: float = 0.0  # sway speed
        self.r: float = 0.0  # yaw rate

    # region Properties
    @property
    def Xn(self):
        Xn = self.position.Xn
        if Xn is None or not isinstance(Xn, float):
            err_msg = f"Xn is supposed to be of type float, it is instead [{type(Xn)}] with value [{Xn}]!"
            logger.critical(err_msg)
            raise ValueError(err_msg)

        return Xn

    @property
    def Yn(self):
        Yn = self.position.Yn
        if Yn is None or not isinstance(Yn, float):
            err_msg = f"Yn is supposed to be of type float, it is instead [{type(Yn)}] with value [{Yn}]!"
            logger.critical(err_msg)
            raise ValueError(err_msg)

        return Yn

    @property
    def state_vector(self) -> np.ndarray:
        """(Equation 1)

        Returns:
            np.ndarray: A vector in R⁶ describing the current state vector of the ship.
        """
        return np.concatenate((self.eta, self.nu))

    @property
    def eta(self) -> np.ndarray:
        """Return position and heading vector in Earth-fixed frame."""
        return np.array([self.Xn, self.Yn, self.psi])

    @property
    def nu(self) -> np.ndarray:
        """Return position and heading vector in body-fixed frame."""
        self.position.ned_offset_from(self.origin_position)
        return np.array([self.u, self.v, self.r])

    # endregion

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

    def get_body_referenced_coordinates(self, reference) -> tuple[float, float]:
        Xb, Yb = self.position._get_body_referenced_coordinates(
            reference=reference,
            heading_psi=self.psi
        )
        return (Xb, Yb)

    # TODO
    ...
