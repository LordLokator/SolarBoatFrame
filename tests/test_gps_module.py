# --- .tests/test_gps_module.py ---

import unittest
import threading
from gps_coordinate import GPSPoint, ShipPosition, BuoyPosition, ObjectiveCoordinate


class TestGPSPoint(unittest.TestCase):
    def test_get_set_coordinates(self):
        p = GPSPoint(1.0, 2.0)
        p.set_coordinates(3.0, 4.0)
        self.assertEqual(p.get_coordinates(), (3.0, 4.0))

    def test_haversine_distance(self):
        p1 = GPSPoint(0, 0)
        p2 = GPSPoint(0, 1)
        self.assertTrue(110000 < p1.haversine_distance(p2) < 112000)


class TestShipPosition(unittest.TestCase):
    def test_singleton_property(self):
        p1 = ShipPosition(1.0, 2.0)
        p2 = ShipPosition(3.0, 4.0)
        self.assertIs(p1, p2)

    def test_thread_safety_update(self):
        ship = ShipPosition(0.0, 0.0)

        def thread_job():
            for _ in range(100):
                ship.update_position(1.0, 2.0)
                ship.update_position(3.0, 4.0)

        threads = [threading.Thread(target=thread_job) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        lat, lon = ship.get_coordinates()
        self.assertIn((lat, lon), [(1.0, 2.0), (3.0, 4.0)])


class TestBuoyPosition(unittest.TestCase):
    def test_within_radius(self):
        buoy = BuoyPosition(0, 0, 150000)  # 150km
        p = GPSPoint(0, 1)
        self.assertTrue(buoy.is_within_radius(p))


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


if __name__ == '__main__':
    unittest.main()
