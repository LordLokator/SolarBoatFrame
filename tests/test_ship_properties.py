# tests/test_ship_properties.py

import unittest
from ship_state.ship_properties import BlueLadyShipProperties
from dataclasses import FrozenInstanceError


class TestGPSPoint(unittest.TestCase):

    def test_constructor(self):
        props = BlueLadyShipProperties(
            breadth=...,
            displacement=...,
            draft=...,
            length=...,
            x_g=...,
        )

        self.assertTrue(props)

    def test_frozen_attributes(self):
        # Test ship properties' immutability

        props = BlueLadyShipProperties()

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
