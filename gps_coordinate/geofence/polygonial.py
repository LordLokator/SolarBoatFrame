from .base import Geofence
from ..base import GPSPoint


class PolygonalGeofence(Geofence):
    def __init__(self, vertices: list[GPSPoint]):
        if len(vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")
        self.vertices = vertices

    def contains(self, point: GPSPoint) -> bool:
        x, y = point.get_coordinates()
        num = len(self.vertices)
        inside = False

        p1x, p1y = self.vertices[0].get_coordinates()
        for i in range(1, num + 1):
            p2x, p2y = self.vertices[i % num].get_coordinates()
            if min(p1y, p2y) < y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    xinters = ((y - p1y) * (p2x - p1x)) / (p2y - p1y + 1e-10) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
            p1x, p1y = p2x, p2y

        return inside
