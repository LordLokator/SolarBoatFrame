import unittest
from pyproj import Transformer
from math import radians, sqrt
from gps_coordinate import ShipPosition, GPSPoint
from gps_coordinate.geofence.circular import CircularGeofence
from ship_state.ship_state import ShipState

from gps_coordinate.config import (
    WGS84_GPS,
    EPSG_32633_BALATON
)

# 12°E and 18°E
DEFAULT_LAT = 17.689868910309883
DEFAULT_LON = 46.7937317098759


class TestCoordinateTransformations(unittest.TestCase):
    def setUp(self):
        self.origin_lat = DEFAULT_LAT
        self.origin_lon = DEFAULT_LON
        self.origin = GPSPoint(self.origin_lat, self.origin_lon)

        self.transformer_to_utm = Transformer.from_crs(WGS84_GPS, EPSG_32633_BALATON, always_xy=True)
        self.transformer_to_wgs = Transformer.from_crs(EPSG_32633_BALATON, WGS84_GPS, always_xy=True)

        self.geofence = CircularGeofence(self.origin, 1000)

        self.ship_position = ShipPosition(latitude=self.origin_lat, longitude=self.origin_lon)
        self.ship_state = ShipState(self.ship_position)

    def _move_ship(self, d_north_m=0, d_east_m=0):
        x0, y0 = self.transformer_to_utm.transform(self.origin_lon, self.origin_lat)
        x1 = x0 + d_east_m
        y1 = y0 + d_north_m
        lon1, lat1 = self.transformer_to_wgs.transform(x1, y1)

        self.ship_position.latitude = lat1
        self.ship_position.longitude = lon1

    def test_initial_body_fixed_coordinates(self):
        """Xb, Yb at origin should be (0, 0) regardless of heading."""

        reference = GPSPoint(self.origin_lat, self.origin_lon)  # Same coordinates

        self.psi = 0.0

        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference=reference)

        self.assertAlmostEqual(Xb, 0.0)
        self.assertAlmostEqual(Yb, 0.0)

    def test_north_displacement_zero_heading(self):
        """Move north with 0 rad heading: Xb should be positive"""
        self._move_ship(d_north_m=10)
        self.ship_state.psi = 0.0
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertGreater(Xb, 0.0)

        # TODO:
        # AssertionError: 0.2556750616058707 != 0.0 within 2 places (0.2556750616058707 difference)
        self.assertAlmostEqual(Yb, 0.0)

    def test_east_displacement_zero_heading(self):
        self._move_ship(d_east_m=10)
        self.ship_state.psi = 0.0
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertAlmostEqual(Xb, 0.0)
        self.assertGreater(Yb, 0.0)

    def test_north_displacement_with_heading_pi_over_2(self):
        self._move_ship(d_north_m=10)
        self.ship_state.psi = radians(90)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertAlmostEqual(Xb, 0.0)
        self.assertLess(Yb, 0.0)  # Rotated frame: North appears as -Yb

    def test_east_displacement_with_heading_pi_over_2(self):
        self._move_ship(d_east_m=10)
        self.ship_state.psi = radians(90)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertGreater(Xb, 0.0)
        self.assertAlmostEqual(Yb, 0.0)

    def test_diagonal_northeast_displacement(self):
        self._move_ship(d_north_m=10, d_east_m=10)
        self.ship_state.psi = radians(45)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        hyp = sqrt(10**2 + 10**2)
        self.assertAlmostEqual(Xb, hyp, delta=0.5)
        self.assertAlmostEqual(Yb, 0.0, delta=0.5)

    def test_heading_wraparound(self):
        """Test heading > 2π has same result as modulo"""
        self._move_ship(d_north_m=10)
        self.ship_state.psi = radians(360)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb1, Yb1 = self.ship_state.get_body_referenced_coordinates(reference)
        self.ship_state.psi = 0.0
        Xb2, Yb2 = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertAlmostEqual(Xb1, Xb2, places=3)
        self.assertAlmostEqual(Yb1, Yb2, places=3)

    def test_negative_heading(self):
        """Negative heading should rotate in the opposite direction"""
        self._move_ship(d_east_m=10)
        self.ship_state.psi = radians(-90)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertLess(Xb, 0.0)
        self.assertAlmostEqual(Yb, 0.0)


if __name__ == "__main__":
    unittest.main()
