# tests/test_managers/test_4g.py

import unittest

from managers import LTEManager


class TestEquationShipState(unittest.TestCase):

    def test_constructor(self):

        with self.assertRaises(NotImplementedError):
            _ = LTEManager()

    def test_connect_success(self):
        ...
        # TODO test cases once LTE implemented


if __name__ == '__main__':
    unittest.main()
