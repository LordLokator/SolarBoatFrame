# tests/test_gps_module.py

import unittest
from ship_state.ship_properties import ShipProperties

# Szántódi rév
SZANTOD_LAT = 46.87993481783788
SZANTOD_LON = 17.89972984313507


class TestGPSPoint(unittest.TestCase):
    def test_constructor(self):
        props = ShipProperties(
            breadth=...,
            displacement=...,
            draft=...,
            length=...,
            x_g=...,
        )

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
