# ship_state/ship_state.py
"""Ide kellenek a dinamikus tulajdonságok."""

from gps_coordinate import ObjectiveCoordinate, ShipPosition


class ShipState:
    """Manages the dynamic properties of the ship, like current position

    Returns:
        _type_: _description_
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.current_position: ShipPosition = ShipPosition()
        self.route: list[ObjectiveCoordinate] = [] # init?

        # TODO
        ...
