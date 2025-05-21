# tests/test_gps_module.py

from copy import deepcopy as copy
import unittest
from gps_coordinate.base import GPSPoint
from ship_state.ship_state import ShipState

# Szántódi rév
SZANTOD_LAN = 46.87993481783788
SZANTOD_LON = 17.89972984313507


class TestGPSPoint(unittest.TestCase):
    def test_constructor(self):
        starting_positio = GPSPoint(copy(SZANTOD_LAN), copy(SZANTOD_LON))
        props = ShipState(starting_positio)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
