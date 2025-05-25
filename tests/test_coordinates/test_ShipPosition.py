# tests/test_gps_module.py

import os
import time
import unittest
import threading
from unittest.mock import MagicMock
from gps_coordinate import GPSPoint, ShipPosition
from gps_coordinate.geofence.circular import CircularGeofence

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


class TestShipPosition(unittest.TestCase):

    # @patch('managers.gps_sensor.gps_manager.GPSManager')
    def test_singleton_property(self):
        mock_gps = MagicMock()
        mock_gps.get_live_location.return_value = (BMEK_LAT, BMEK_LON)

        _fence = CircularGeofence(
            GPSPoint(BMEK_LAT, BMEK_LON),
            1_000_000  # 1000km
        )

        p1 = ShipPosition(_fence, mock_gps)
        p2 = ShipPosition(_fence, mock_gps)

        self.assertIs(p1, p2)

    def test_thread_safety_update(self):

        ship = ShipPosition(
            geofence=CircularGeofence(
                GPSPoint(BMEK_LAT, BMEK_LON),
                1_000_000  # 1000km
            )
        )

        time.sleep(.5)

        def thread_job():
            for i in range(10):
                lat, lon = (SZANTOD_LAT, SZANTOD_LON) if i % 2 == 0 else (TIHANY_LAT, TIHANY_LON)
                pos = GPSPoint(lat, lon)
                success = ship.set_ship_position(pos)
                assert success, f"GeofenceR: {ship.geofence.radius} | H_dist: {ship.geofence.center.haversine_distance(pos)}"

        threads = [threading.Thread(target=thread_job) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        lat, lon = ship.get_coordinates()
        self.assertIn(
            (lat, lon),
            [
                (SZANTOD_LAT, SZANTOD_LON),
                (TIHANY_LAT, TIHANY_LON)
            ] # Because we *did* change it. We don't know which change was last.
        )

    def test_project_earthbased(self):
        point = GPSPoint(BMEK_LAT, BMEK_LON)

        self.assertAlmostEqual(point.Xn, BMEK_X_32634, places=3)
        self.assertAlmostEqual(point.Yn, BMEK_Y_32634, places=3)


if __name__ == '__main__':
    unittest.main()
