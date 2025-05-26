# tests/test_managers/test_4g.py

import unittest

from managers import LTEManager


class TestEquationShipState(unittest.TestCase):

    def test_constructor(self):
        lte_manager = LTEManager()
        self.assertTrue(lte_manager)

    def test_connect_success(self):
        ...
        # TODO test cases once LTE implemented


if __name__ == '__main__':
    unittest.main()
