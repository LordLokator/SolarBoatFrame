from .base import Geofence
from ..base import GPSPoint


class CircularGeofence(Geofence):
    def __init__(self, center: GPSPoint, radius_m: float):
        self.center = center
        self.radius = radius_m

    def contains(self, point: GPSPoint) -> bool:
        return self.center.haversine_distance(point) <= self.radius
