# tests/test_managers.gps_sensor.gps_manager.py

import os
import unittest
from unittest.mock import MagicMock, patch
from managers import GPSManager
from loguru import logger

LOG_PATH = os.path.abspath(os.path.join("logging", "gps_manager.log"))
logger.add(
    LOG_PATH,
    level="WARNING",
    backtrace=True,
    diagnose=True
)


class TestGPSManager(unittest.TestCase):

    def setUp(self):
        self.patcher_serial = patch('managers.gps_sensor.gps_manager.Serial')
        self.patcher_ubxreader = patch('managers.gps_sensor.gps_manager.UBXReader')

        self.mock_serial = self.patcher_serial.start()
        self.mock_ubxreader_cls = self.patcher_ubxreader.start()

    def tearDown(self):
        self.patcher_serial.stop()
        self.patcher_ubxreader.stop()

    def test_initialization(self):
        mock_reader = MagicMock()
        mock_reader.read.return_value = (b'', MagicMock(lat=50.0, lon=8.0))
        self.mock_ubxreader_cls.return_value = mock_reader

        gps = GPSManager()
        self.mock_serial.assert_called_once()
        self.mock_ubxreader_cls.assert_called_once()
        self.assertIsNotNone(gps.stream)
        self.assertIsNotNone(gps.ubr)
        gps.close()

    def test_get_location_valid(self):
        mock_reader = MagicMock()
        mock_reader.read.return_value = (b'', MagicMock(lat=50.0, lon=8.0))
        self.mock_ubxreader_cls.return_value = mock_reader

        gps = GPSManager()
        lat, lon, heading = gps.get_live_location()
        self.assertEqual(lat, 50.0)
        self.assertEqual(lon, 8.0)
        gps.close()

    def test_get_location_exception(self):
        mock_reader = MagicMock()
        mock_reader.read.side_effect = Exception("Read failed")
        self.mock_ubxreader_cls.return_value = mock_reader

        gps = GPSManager()
        lat, lon, heading = gps.get_live_location()
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        gps.close()


if __name__ == "__main__":
    unittest.main()
