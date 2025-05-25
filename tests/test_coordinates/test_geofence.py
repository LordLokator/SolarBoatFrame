# tests/test_geofence.py

import unittest
from gps_coordinate.geofence.circular import CircularGeofence
from gps_coordinate.geofence.polygonal import PolygonalGeofence
from gps_coordinate.base import GPSPoint


class TestCircularGeofence(unittest.TestCase):

    def setUp(self):
        self.center = GPSPoint(47.4979, 19.0402)  # Budapest
        self.geofence = CircularGeofence(center=self.center, radius_m=1000)

    def test_point_inside_circle(self):
        inside_point = GPSPoint(47.4989, 19.0410)
        self.assertTrue(self.geofence.contains(inside_point))

    def test_point_outside_circle(self):
        outside_point = GPSPoint(47.5100, 19.0400)
        self.assertFalse(self.geofence.contains(outside_point))

    def test_point_on_boundary(self):
        edge_point = GPSPoint(47.4899, 19.0402)  # ~1km south
        self.assertTrue(self.geofence.contains(edge_point))


class TestPolygonalGeofence(unittest.TestCase):

    def setUp(self):
        self.vertices = [
            GPSPoint(47.4970, 19.0400),
            GPSPoint(47.4970, 19.0500),
            GPSPoint(47.5030, 19.0500),
            GPSPoint(47.5030, 19.0400)
        ]
        self.geofence = PolygonalGeofence(vertices=self.vertices)

    def test_point_inside_polygon(self):
        inside_point = GPSPoint(47.4999, 19.0450)
        self.assertTrue(self.geofence.contains(inside_point))

    def test_point_outside_polygon(self):
        outside_point = GPSPoint(47.5100, 19.0600)
        self.assertFalse(self.geofence.contains(outside_point))

    def test_point_on_edge_contains(self):
        edge_point = GPSPoint(47.4970, 19.0450)
        self.assertFalse(self.geofence.contains(edge_point))  # Don't accept as "inside"

    def test_point_on_edge_covers(self):
        # Use 'geofence._covers' if the vertecies and sides of the polygon are acceptable.

        edge_point = GPSPoint(47.4970, 19.0450)
        self.assertTrue(self.geofence._covers(edge_point))  # Accept as "inside"


if __name__ == "__main__":
    unittest.main()
