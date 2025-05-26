# tests/test_equations_validation/test_eq_shipposition.py

# tests/test_gps_module.py

import os
import unittest
from unittest.mock import MagicMock, patch

from pyproj import Transformer
from gps_coordinate import (
    GPSPoint,
    CircularGeofence
)
from ship import ShipPosition

from gps_coordinate.config import (
    WGS84_GPS,
    EPSG_32634_BP
)

from loguru import logger

LOG_PATH = os.path.abspath(os.path.join("logging", "test_gps_module.log"))

logger.add(
    LOG_PATH,
    level="WARNING",
    backtrace=True,
    diagnose=True
)


DEFAULT_LAT = 0.0
DEFAULT_LON = 0.0


class TestShipPosition(unittest.TestCase):

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

    # @patch('managers.gps_sensor.gps_manager.GPSManager')
    def test_singleton_property(self):
        ...

        self.assertIs(..., ...)


if __name__ == '__main__':
    unittest.main()
