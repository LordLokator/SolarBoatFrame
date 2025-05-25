# tests/test_gps_module.py

import os
import unittest
from copy import deepcopy as copy
from gps_coordinate import GPSPoint, BuoyPosition, ObjectiveCoordinate

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


class TestBuoyPosition(unittest.TestCase):
    def test_within_radius(self):

        # Tihanyi rév
        lat_1 = copy(TIHANY_LAT)
        lon_1 = copy(TIHANY_LON)

        buoy = BuoyPosition(lat_1, lon_1, 2000)  # 2km [real: 1.1km]

        # Szántódi rév
        lat_2 = copy(SZANTOD_LAT)
        lon_2 = copy(SZANTOD_LON)
        p = GPSPoint(lat_2, lon_2)

        self.assertTrue(buoy.is_within_radius(p))

    def test_outside_radius(self):

        # Tihanyi rév
        lat_1 = copy(TIHANY_LAT)
        lon_1 = copy(TIHANY_LON)

        buoy = BuoyPosition(lat_1, lon_1, 100)  # 100m [real: 1100m]

        # Szántódi rév
        lat_2 = copy(SZANTOD_LAT)
        lon_2 = copy(SZANTOD_LAT)
        p = GPSPoint(
            latitude=lat_2,
            longitude=lon_2
        )

        self.assertTrue(not buoy.is_within_radius(p))


if __name__ == '__main__':
    unittest.main()
