# tests/test_gps_module.py

import unittest
from ship_state.ship_properties import ShipProperties

# Szántódi rév
SZANTOD_LAN = 46.87993481783788
SZANTOD_LON = 17.89972984313507


class TestGPSPoint(unittest.TestCase):
    def test_constructor(self):
        props = ShipProperties()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
