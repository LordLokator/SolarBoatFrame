from ship_state.ship_properties import ShipProperties
from ship_state.ship_state import ShipState


class ShipManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.ship_properties = ShipProperties()
        self.ship_state = ShipState()

        # TODO
        ...

    def get_next_objective_coo(self):
        return self.ship_state.route[0]
