# tests/test_gps_module.py

import os
import unittest
from gps_coordinate import ObjectiveCoordinate

from loguru import logger
LOG_PATH = os.path.abspath(os.path.join("logging", "test_gps_module.log"))

logger.add(
    LOG_PATH,
    level="WARNING",
    backtrace=True,
    diagnose=True
)

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
