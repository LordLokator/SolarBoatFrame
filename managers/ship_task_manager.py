from loguru import logger
from gps_coordinate import CircularGeofence
from gps_coordinate import ObjectiveCoordinate
from gps_coordinate import ShipPosition
from gps_coordinate import GPSPoint
from ship_state.ship_properties import BlueLadyShipProperties
from ship_state.ship_state import ShipState


class ShipTaskManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.ship_properties = BlueLadyShipProperties()

        _geofence_center = GPSPoint(47.47, 19.03)  # ~ Kelenföld
        geofence_huge = CircularGeofence(center=_geofence_center, radius_m=30_000)  # 30km
        starting_position = ShipPosition(geofence=geofence_huge)
        self.ship_state = ShipState(starting_position)

        # TODO
        ...

    def step(self) -> None:
        print(self.ship_state.position)

    def get_next_objective_coo(self) -> ObjectiveCoordinate:
        if len(self.ship_state.route) < 1:
            logger.warning(f"ShipState has no more objectives in route list!")
            return None

        return self.ship_state.route[0]
