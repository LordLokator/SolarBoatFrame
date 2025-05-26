# tests/test_equations_validation/test_eq_shipstate.py

import unittest
from unittest.mock import MagicMock, patch

from pyproj import Transformer
from gps_coordinate.base import GPSPoint
from gps_coordinate.geofence.circular import CircularGeofence
from ship import (
    ShipPosition,
    ShipState
)

from gps_coordinate.config import (
    WGS84_GPS,
    EPSG_32634_BP
)


DEFAULT_LAT = 0.0
DEFAULT_LON = 0.0


class TestEquationShipState(unittest.TestCase):

    def setUp(self):
        # Start patching
        patcher = patch('managers.gps_sensor.gps_manager.GPSManager')
        self.mock_gpsmanager_cls = patcher.start()
        self.addCleanup(patcher.stop)  # Ensure cleanup

        # transformers between Coordinate systems
        self.transformer_to_utm = Transformer.from_crs(WGS84_GPS, EPSG_32634_BP, always_xy=True)
        self.transformer_to_wgs = Transformer.from_crs(EPSG_32634_BP, WGS84_GPS, always_xy=True)

        # Mock GPSManager behavior
        mock_gps = MagicMock()
        mock_gps.get_live_location.return_value = (DEFAULT_LAT, DEFAULT_LON)
        self.mock_gpsmanager_cls.return_value = mock_gps

        self.geofence = CircularGeofence(
            center=GPSPoint(DEFAULT_LAT, DEFAULT_LON),
            radius_m=1000  # 1km
        )

        self.ship_position = ShipPosition(self.geofence, mock_gps)
        self.ship_state = ShipState(
            starting_position=self.ship_position
        )

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

    def test_constructor(self):
        ...

        self.assertTrue(...)


if __name__ == '__main__':
    unittest.main()
