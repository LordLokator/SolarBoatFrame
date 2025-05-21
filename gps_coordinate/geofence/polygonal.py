from shapely.geometry import Point, Polygon
from .base import Geofence
from ..base import GPSPoint


class PolygonalGeofence(Geofence):
    def __init__(self, vertices: list[GPSPoint]):
        if len(vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")

        self.vertices = vertices
        self._polygon = Polygon([v.get_coordinates() for v in vertices])

    def contains(self, point: GPSPoint) -> bool:
        shapely_point = Point(point.get_coordinates())
        return self._polygon.contains(shapely_point)

    def _covers(self, point: GPSPoint) -> bool:
        # Use if the vertecies and sides of the polygon are acceptable.

        shapely_point = Point(point.get_coordinates())
        return self._polygon.covers(shapely_point)
