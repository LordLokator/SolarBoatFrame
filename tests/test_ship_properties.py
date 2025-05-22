# tests/test_gps_module.py

import unittest
from ship_state.ship_properties import ShipProperties
from dataclasses import FrozenInstanceError

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

    def test_frozen_attributes(self):
        # Test ship properties' immutability

        props = ShipProperties()

        with self.assertRaises(FrozenInstanceError):
            props.length = 20.0

        with self.assertRaises(FrozenInstanceError):
            props.breadth = 20.0

        with self.assertRaises(FrozenInstanceError):
            props.draft = 20.0

        with self.assertRaises(FrozenInstanceError):
            props.displacement = 20.0

        with self.assertRaises(FrozenInstanceError):
            props.x_g = 20.0


if __name__ == '__main__':
    unittest.main()
