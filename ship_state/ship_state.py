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
        self.origin_position: ShipPosition = starting_position
        self.current_position: ShipPosition = starting_position
        self.route: list[ObjectiveCoordinate] = []  # init?
        self.properties = BlueLadyShipProperties()

        self.psi: float = 0.0  # heading in radians (w.r.t North)
        self.u: float = 0.0  # surge speed
        self.v: float = 0.0  # sway speed
        self.r: float = 0.0  # yaw rate

    # region Properties
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
        self.current_position.ned_offset_from(self.origin_position)
        return np.array([self.u, self.v, self.r])

    # endregion

    def eta_dot(self) -> np.ndarray:
        """Calculate Earth-frame velocity \u03b7_dot = R(psi) * nu (Equation 2)."""
        R = self.rotation_matrix()
        nu = self.nu()
        return R @ nu
    
    def nu_dot(self) -> np.ndarray:
        #TODO: implement this function
        return np.array([0, 0, 0])

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
        Xb, Yb = self.current_position._get_body_referenced_coordinates(
            reference=reference,
            heading_psi=self.psi
        )
        return (Xb, Yb)

    def psi_k(self, index_of_current_segment: float) -> float:
        """return the segment heading angle IN RADIANS of the current and the next segment (equation 4)."""
        if self.route is None or len(self.route) < 2:
            err_msg = "Route is not set or has less than 2 points!"
            logger.critical(err_msg)
            raise ValueError(err_msg)
        if index_of_current_segment is None or index_of_current_segment < 0 or index_of_current_segment >= len(self.route):
            err_msg = "Current segment is not given or out of bounds!"
            logger.critical(err_msg)
            raise ValueError(err_msg)
        if  index_of_current_segment == len(self.route) - 1:
            err_msg = "Current segment is the last one in the route, cannot calculate heading of next segment!"
            logger.critical(err_msg)
            raise IndexError(err_msg)
        current_segment = self.route[index_of_current_segment]
        next_segment = self.route[index_of_current_segment + 1]
        return np.atan2(
            next_segment.Yn - current_segment.Yn,
            next_segment.Xn - current_segment.Xn
        )
    
    def L_k(self, index_of_current_segment: float) -> float:
        """return the distance before a waypoint at which a turning maneuver should start (equation 5)."""
        psi_k_radian = self.psi_k(index_of_current_segment)
        psi_k1_radian = self.psi_k(index_of_current_segment + 1)
        if psi_k_radian is None or psi_k1_radian is None:
            err_msg = "psi_k or psi_k1 is None!"
            logger.critical(err_msg)
            raise ValueError(err_msg)
        delta_psi = psi_k1_radian - psi_k_radian
        a6 = 5.987527e-09
        a5 = -1.561371e-06
        a4 = 1.430259e-04
        a3 = -0.004935727
        a2 = 0.01235089
        a1 = 2.10745127
        a0 = -0.02348713
        #this is the equation 49 from the paper
        # TODO: check the coefficients AND the units : degree or radian?
        return a6 * delta_psi**6 + a5 * delta_psi**5 + a4 * delta_psi**4 + a3 * delta_psi**3 + a2 * delta_psi**2 + a1 * delta_psi + a0

    def S_c(delta_c: float, ngc: float) -> np.ndarray:
        """
        Compute the control signal vector S_c(t) = [δ_c(t), n_gc(t)]ᵀ (Equation 6).

        Args:
            delta_c (float): Commanded rudder angle (in radians).
            ngc (float): Commanded propeller shaft speed (in RPM).

        Returns:
            np.ndarray: Control vector [δ_c, n_gc].
        """
        return np.array([delta_c, ngc])
    
    def matrix_M(self) -> np.ndarray:
        """return the inertia matrix M (Equation 8)."""
        #TODO: fill in the values
        m11 = none
        m22 = none
        m23 = none
        m32 = none
        m33 = none
        
        return np.array([
            [m11, 0, 0],
            [0, m22, m23],
            [0, m32, m33]
        ])
    
    def matrix_C(self) -> np.ndarray:
        """return the Coriolis and centripetal matrix C (Equation 9)."""
        #TODO: fill in the values
        c13 = none
        c23 = none
        c31 = none
        c32 = none
        
        return np.array([
            [0, 0, c13],
            [0, 0, c23],
            [c31, c32, 0]
        ])
        
    def matrix_D(self) -> np.ndarray:
        """return the damping matrix D (Equation 10)."""
        d11 = none
        d22 = none
        d23 = none
        d32 = none
        d33 = none
        #TODO: fill in the values
        return np.array([
            [-d11, 0, 0],
            [0, -d22, -d23],
            [0, -d32, -d33]
        ])
        
    def force_vector(self) -> np.ndarray:
        return self.matrix_M() @ self.nu_dot() + self.matrix_C() @ self.nu() + self.matrix_D() @ self.nu()
        
        
        
        
    # TODO
    ...
