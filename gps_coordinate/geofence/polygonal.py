from shapely.geometry import Point, Polygon
from .base import Geofence
from ..base import GPSPoint
import numpy as np

def _are_collinear(coords: list[float]):
    a, b = np.array(coords[0]), np.array(coords[1])
    ab = b - a
    return all(np.isclose(np.cross(ab, np.array(p) - a), 0) for p in coords[2:])

class PolygonalGeofence(Geofence):
    def __init__(self, vertices: list[GPSPoint]):
        if len(vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")

        self.coordinates = [v.get_coordinates() for v in vertices]  # store lat-lon

        if _are_collinear(self.coordinates):
            raise ValueError("Vertices are on a line!")

        self._polygon = Polygon(self.coordinates)

        if not (self._polygon.is_valid and self._polygon.area > 0):
            raise ValueError("Invalid Polygon!")

    def contains(self, point: GPSPoint) -> bool:
        shapely_point = Point(point.get_coordinates())
        return self._polygon.contains(shapely_point)

    def _covers(self, point: GPSPoint) -> bool:
        # Use if the vertecies and sides of the polygon are acceptable.

        shapely_point = Point(point.get_coordinates())
        return self._polygon.covers(shapely_point)
