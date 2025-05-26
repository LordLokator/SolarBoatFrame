import unittest
from unittest.mock import MagicMock, patch
from pyproj import Transformer
from math import radians, sqrt
from gps_coordinate import ShipPosition, GPSPoint
from gps_coordinate.geofence.circular import CircularGeofence
from ship.ship_state import ShipState

from gps_coordinate.config import (
    WGS84_GPS,
    EPSG_32633_BALATON,
    EPSG_32634_BP,
    EPSG_32632_MONACO
)

DEFAULT_LAT = 0.0
DEFAULT_LON = 0.0


class TestCoordinateTransformations(unittest.TestCase):
    def setUp(self):
        # Start patching
        patcher = patch('managers.gps_sensor.gps_manager.GPSManager')
        self.mock_gpsmanager_cls = patcher.start()
        self.addCleanup(patcher.stop)  # Ensure cleanup

        # Mock GPSManager behavior
        mock_gps = MagicMock()
        mock_gps.get_live_location.return_value = (DEFAULT_LAT, DEFAULT_LON)
        self.mock_gpsmanager_cls.return_value = mock_gps

        # Set up test objects
        self.origin_lat = DEFAULT_LAT
        self.origin_lon = DEFAULT_LON
        self.origin = GPSPoint(self.origin_lat, self.origin_lon)

        self.transformer_to_utm = Transformer.from_crs(WGS84_GPS, EPSG_32634_BP, always_xy=True)
        self.transformer_to_wgs = Transformer.from_crs(EPSG_32634_BP, WGS84_GPS, always_xy=True)

        self.geofence = CircularGeofence(self.origin, 3333)

        self.ship_position = ShipPosition(self.geofence, mock_gps)
        self.ship_state = ShipState(self.ship_position)

    def _move_ship(self, d_north_m=0, d_east_m=0):
        """Moves the lat-lon for the self.ship_position object using the two params. \
        Does so by transforming between GPS and UTM.

        Args:
            d_north_m (int, optional): Move N-S. Defaults to 0.
            d_east_m (int, optional): Move E-W. Defaults to 0.
        """
        x0, y0 = self.transformer_to_utm.transform(self.origin_lon, self.origin_lat)
        x1 = x0 + d_east_m
        y1 = y0 + d_north_m
        lon1, lat1 = self.transformer_to_wgs.transform(x1, y1)

        self.ship_position.latitude = lat1
        self.ship_position.longitude = lon1

    def test_initial_body_fixed_coordinates(self):
        """Xb, Yb at origin should be (0, 0) regardless of heading."""
        self._move_ship(
            d_east_m=0,
            d_north_m=0
        )

        reference = GPSPoint(self.origin_lat, self.origin_lon)  # Same coordinates

        self.psi = 0.0

        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference=reference)

        # AssertionError: 69.99999999999997 != 0.0 within 3 places (69.99999999999997 difference)
        self.assertAlmostEqual(Xb, 0.0, places=3)
        self.assertAlmostEqual(Yb, 0.0, places=3)

    def test_north_displacement_zero_heading(self):
        """Move north with 0 rad heading: Xb should be positive"""
        self._move_ship(d_north_m=10)
        self.ship_state.psi = 0.0
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertGreater(Xb, 0.0)

        self.assertAlmostEqual(Yb, 0.0, places=3)

    def test_east_displacement_zero_heading(self):
        self._move_ship(d_east_m=20)
        self.ship_state.psi = 0.0
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertAlmostEqual(Xb, 0.0, places=3)
        self.assertGreater(Yb, 0.0)

    def test_north_displacement_with_heading_pi_over_2(self):
        MOVEMENT = 30  # m
        self._move_ship(d_north_m=MOVEMENT)
        self.ship_state.psi = radians(90)

        reference = GPSPoint(self.origin_lat, self.origin_lon)

        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)

        self.assertAlmostEqual(Xb, 0.0, delta=0.5)
        self.assertAlmostEqual(Yb, -MOVEMENT, delta=0.5)

    def test_east_displacement_with_heading_pi_over_2(self):
        self._move_ship(d_east_m=40)
        self.ship_state.psi = radians(90)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertGreater(Xb, 0.0)
        self.assertAlmostEqual(Yb, 0.0, places=3)

    def test_diagonal_northeast_displacement(self):
        self.ship_position.update_positin_with_gps_data()

        d_north = 50
        d_east = 50
        hyp = sqrt(d_north**2 + d_east**2)

        self._move_ship(d_north_m=d_north, d_east_m=d_east)
        self.ship_state.psi = radians(45)

        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)

        self.assertAlmostEqual(Xb, hyp, delta=0.5)
        self.assertAlmostEqual(Yb, 0.0, delta=0.5)
        # 0.0 is the target because we turn 45° -> the 'right hand' coordinate is 0!

    def test_heading_wraparound(self):
        """Test heading > 2π has same result as modulo"""
        self._move_ship(d_north_m=70)
        self.ship_state.psi = radians(360)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb1, Yb1 = self.ship_state.get_body_referenced_coordinates(reference)
        self.ship_state.psi = 0.0
        Xb2, Yb2 = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertAlmostEqual(Xb1, Xb2, places=3)
        self.assertAlmostEqual(Yb1, Yb2, places=3)

    def test_negative_heading(self):
        """Negative heading should rotate in the opposite direction"""
        self._move_ship(d_east_m=80)
        self.ship_state.psi = radians(-90)
        reference = GPSPoint(self.origin_lat, self.origin_lon)
        Xb, Yb = self.ship_state.get_body_referenced_coordinates(reference)
        self.assertLess(Xb, 0.0)
        self.assertAlmostEqual(Yb, 0.0, places=3)


if __name__ == "__main__":
    unittest.main()
