# tests/test_gps_module.py

import os
import time
import unittest
from unittest.mock import MagicMock, patch
from managers import GPSManager

from loguru import logger
LOG_PATH = os.path.abspath(os.path.join("logging", "test_gps_module.log"))

logger.add(
    LOG_PATH,
    level="WARNING",
    backtrace=True,
    diagnose=True
)

# Tihanyi rév [EPSG:4326]
TIHANY_LAT = 46.88868997786068
TIHANY_LON = 17.89171566948177


class TestGPSModule(unittest.TestCase):

    @patch('managers.gps_sensor.gps_manager.Serial')
    @patch('managers.gps_sensor.gps_manager.UBXReader')
    def test_initialization(self, mock_ubxreader, mock_serial):
        gps = GPSManager()
        mock_serial.assert_called_once()
        mock_ubxreader.assert_called_once()
        self.assertIsNotNone(gps.stream)
        self.assertIsNotNone(gps.ubr)
        gps.close()

    @patch('managers.gps_sensor.gps_manager.Serial')
    @patch('managers.gps_sensor.gps_manager.UBXReader')
    def test_get_live_location(self, mock_ubxreader_cls, mock_serial):
        mock_reader = MagicMock()

        def delayed_read():
            time.sleep(2)  # Simulate timeout or delay
            return (b'', MagicMock(lat=50.0, lon=8.0))

        mock_reader.read.side_effect = delayed_read
        mock_ubxreader_cls.return_value = mock_reader

        lat, lon = GPSManager().get_live_location()

        self.assertAlmostEqual(lat, 50.0)
        self.assertAlmostEqual(lon, 8.0)


if __name__ == "__main__":
    unittest.main()
