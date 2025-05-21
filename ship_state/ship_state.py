# ship_state/ship_state.py
"""Ide kellenek a dinamikus tulajdonságok."""

from gps_coordinate import ObjectiveCoordinate, ShipPosition


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

        self.x: float  # Earth-fixed x
        self.y: float  # Earth-fixed y
        self.psi: float  # heading in radians (w.r.t North)
        self.u: float  # surge speed
        self.v: float  # sway speed
        self.r: float  # yaw rate


        # TODO
        ...
