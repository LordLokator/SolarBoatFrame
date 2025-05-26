# tests/test_managers.gps_sensor.gps_manager.py

import os
import unittest
from unittest.mock import MagicMock, patch
from managers.gps_sensor.gps_manager import GPSManager

from loguru import logger
LOG_PATH = os.path.abspath(os.path.join("logging", "test_managers.gps_sensor.gps_manager.log"))

logger.add(
    LOG_PATH,
    level="WARNING",
    backtrace=True,
    diagnose=True
)


class TestGPSManager(unittest.TestCase):

    @patch('managers.gps_sensor.gps_manager.Serial')
    @patch('managers.gps_sensor.gps_manager.UBXReader')
    def test_initialization(self, mock_ubxreader_cls, mock_serial):
        mock_reader = MagicMock()
        mock_reader.read.return_value = (b'', MagicMock(lat=50.0, lon=8.0))
        mock_ubxreader_cls.return_value = mock_reader

        gps = GPSManager()
        mock_serial.assert_called_once()
        mock_ubxreader_cls.assert_called_once()
        self.assertIsNotNone(gps.stream)
        self.assertIsNotNone(gps.ubr)
        gps.close()

    @patch('managers.gps_sensor.gps_manager.UBXReader')
    def test_get_location_valid(self, mock_ubxreader_cls):
        mock_reader = MagicMock()
        mock_reader.read.return_value = (b'', MagicMock(lat=50.0, lon=8.0))
        mock_ubxreader_cls.return_value = mock_reader

        gps = GPSManager()
        lat, lon = gps.get_live_location()
        self.assertEqual(lat, 50.0)
        self.assertEqual(lon, 8.0)
        gps.close()

    @patch('managers.gps_sensor.gps_manager.UBXReader')
    def test_get_location_exception(self, mock_ubxreader_cls):
        mock_reader = MagicMock()
        mock_reader.read.side_effect = Exception("Read failed")
        mock_ubxreader_cls.return_value = mock_reader

        gps = GPSManager()
        lat, lon = gps.get_live_location()
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        gps.close()


if __name__ == "__main__":
    unittest.main()
