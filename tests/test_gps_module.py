# tests/test_gps_module.py

import os
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
    rotation="500 KB",
    backtrace=True,
    diagnose=True
)

# Tihanyi rév [EPSG:4326]
TIHANY_LAT = 46.88868997786068
TIHANY_LON = 17.89171566948177

# Szántódi rév [EPSG:4326]
SZANTOD_LAT = 46.87993481783788
SZANTOD_LON = 17.89972984313507

# BME K [EPSG:4326]
BMEK_LAT = 47.48147848232312
BMEK_LON = 19.05566975662944

# BME K [EPSG:32633]
BMEK_X = 805448.863469
BMEK_Y = 5266582.869029


class TestGPSPoint(unittest.TestCase):
    def test_get_coordinates(self):
        test_lat = 3.0
        test_lon = 4.0
        p = GPSPoint(test_lat, test_lon)

        self.assertEqual(p.get_coordinates(), (test_lat, test_lon))

    def test_get_set_coordinates(self):
        test_lat = 3.0
        test_lon = 4.0
        secondary = GPSPoint(test_lat, test_lon)

        reference = GPSPoint(1.0, 2.0)
        reference.set_coordinates(secondary)

        self.assertEqual(reference.get_coordinates(), (test_lat, test_lon))

    def test_haversine_distance(self):
        p1 = GPSPoint(0, 0)
        p2 = GPSPoint(0, 1)
        self.assertTrue(110000 < p1.haversine_distance(p2) < 112000)


class TestShipPosition(unittest.TestCase):
    def test_singleton_property(self):
        p1 = ShipPosition(1.0, 2.0)
        p2 = ShipPosition(3.0, 4.0)
        self.assertIs(p1, p2)  # if truly singleton -> this holds

    def test_thread_safety_update(self):
        init_lat = copy(TIHANY_LAT)
        init_lon = copy(TIHANY_LON)

        fence = CircularGeofence(GPSPoint(init_lat, init_lon), 5000)  # 5km

        ship = ShipPosition(init_lat, init_lon, fence)

        def thread_job():
            for _ in range(5):
                success = ship.update_position(ObjectiveCoordinate(
                    copy(SZANTOD_LAT),
                    copy(SZANTOD_LON)
                ))
                assert success, "Geofence stopped you from having a good day!"

        threads = [threading.Thread(target=thread_job) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        lat, lon = ship.get_coordinates()
        self.assertIn((lat, lon), [(copy(SZANTOD_LAT), copy(SZANTOD_LON))])


class TestBuoyPosition(unittest.TestCase):
    def test_within_radius(self):

        # Tihanyi rév
        lan_1 = copy(TIHANY_LAT)
        lon_1 = copy(TIHANY_LON)

        buoy = BuoyPosition(lan_1, lon_1, 2000)  # 2km [real: 1.1km]

        # Szántódi rév
        lan_2 = copy(SZANTOD_LAT)
        lon_2 = copy(SZANTOD_LON)
        p = GPSPoint(lan_2, lon_2)

        self.assertTrue(buoy.is_within_radius(p))

    def test_outside_radius(self):

        # Tihanyi rév
        lan_1 = copy(TIHANY_LAT)
        lon_1 = copy(TIHANY_LON)

        buoy = BuoyPosition(lan_1, lon_1, 100)  # 100m [real: 1100m]

        # Szántódi rév
        lan_2 = copy(SZANTOD_LAT)
        lon_2 = copy(SZANTOD_LAT)
        p = GPSPoint(lan_2, lon_2)

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
