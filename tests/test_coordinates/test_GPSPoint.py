# tests/test_gps_module.py

import os
import unittest
from gps_coordinate import GPSPoint

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

# Szántódi rév [EPSG:4326]
SZANTOD_LAT = 46.87993481783788
SZANTOD_LON = 17.89972984313507

SZANTOD_X_32633 = 720940.9110621361
SZANTOD_Y_32633 = 5195904.446368263

# BME K [EPSG:4326]
BMEK_LAT = 47.48147848232312
BMEK_LON = 19.05566975662944

# BME K [EPSG:32634]
BMEK_X_32634 = 353516.7257719671
BMEK_Y_32634 = 5260503.589850288

# # BME K [EPSG:32633]
# BMEK_X_32633 = 805448.863469
# BMEK_Y_32633 = 5266582.869029


class TestGPSPoint(unittest.TestCase):
    def test_get_coordinates(self):
        test_lat = BMEK_LAT
        test_lon = BMEK_LON
        p = GPSPoint(test_lat, test_lon)

        self.assertEqual(p.get_coordinates(), (test_lat, test_lon))

    def test_get_set_coordinates(self):
        test_lat = BMEK_LAT
        test_lon = BMEK_LON
        secondary = GPSPoint(test_lat, test_lon)

        reference = GPSPoint(BMEK_LAT, BMEK_LON)
        reference.set_coordinates(secondary)

        self.assertEqual(reference.get_coordinates(), (test_lat, test_lon))

    def test_haversine_distance(self):
        p1 = GPSPoint(BMEK_LAT, BMEK_LON)
        p2 = GPSPoint(SZANTOD_LAT, SZANTOD_LON)

        _dist = p1.haversine_distance(p2)
        logger.warning(f"Haversine calculated is [{_dist}]")

        # Distance should be exactly 110_030 meters. Checking for +-50m:
        self.assertTrue(109_980 < _dist < 110_080)

        # Distance should be exactly 110_030 meters. Checking for +-5m:
        self.assertTrue(110_025 < _dist < 110_035)


if __name__ == '__main__':
    unittest.main()
