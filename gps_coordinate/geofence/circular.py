from .base import Geofence
from ..base import GPSPoint
from loguru import logger


class CircularGeofence(Geofence):
    def __init__(self, center: GPSPoint, radius_m: float):
        self.center = center
        self.radius = radius_m

    def contains(self, point: GPSPoint) -> bool:
        _dist = self.center.haversine_distance(point)
        _contains = _dist <= self.radius

        if not _contains:
            logger.error(f"Error at CircularGeofence: R({self.radius}) < Dist({_dist}). \
                         Points: [{self.center}] [{point}]")

        return _contains
