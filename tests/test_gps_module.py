# tests/test_gps_module.py

import os
import time
import unittest
from copy import deepcopy as copy
import threading
from gps_coordinate import GPSPoint, ShipPosition, BuoyPosition, ObjectiveCoordinate
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


class TestShipPosition(unittest.TestCase):
    def test_singleton_property(self):
        _fence = CircularGeofence(
            GPSPoint(BMEK_LAT, BMEK_LON),
            1_000_000  # m
        )
        p1 = ShipPosition(_fence)
        p2 = ShipPosition(_fence)

        time.sleep(1)

        self.assertIs(p1, p2)  # if truly singleton -> this holds

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
                pos = ObjectiveCoordinate(lat, lon)
                success = ship.update_position(pos)
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

        self.assertAlmostEqual(point.Xn, BMEK_X_32634, places=1)
        self.assertAlmostEqual(point.Yn, BMEK_Y_32634, places=1)


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


class TestObjectiveCoordinate(unittest.TestCase):

    def test_label_default(self):
        obj = ObjectiveCoordinate(10, 20)
        self.assertEqual(obj.label, "Unnamed Objective")

    def test_label_custom(self):
        obj = ObjectiveCoordinate(10, 20, "Checkpoint A")
        self.assertEqual(obj.label, "Checkpoint A")

    def test_repr(self):
        obj = ObjectiveCoordinate(10, 20, "Test")
        self.assertIn("ObjectivePoint(label=Test", repr(obj))
        # NOTE: repr -> class.__repr__ dunder method
        # for building canonical string representation
        # https://docs.python.org/3/reference/datamodel.html#object.__repr__


if __name__ == '__main__':
    unittest.main()
