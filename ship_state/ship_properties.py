# ship_state/ship_properties.py
"""Ide kellenek a statikus tulajdonságok, pl hajó merülése, vagy közvetlenül ebből származtatott mennyiségek."""


from gps_coordinate.ship_position import ShipPosition


class ShipProperties:
    _instance = None

    def __new__(cls, starting_position):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, starting_position: ShipPosition):
        self.current_position = starting_position
