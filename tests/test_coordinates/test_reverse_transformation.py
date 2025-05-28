import unittest
from math import isclose

from gps_coordinate import GPSPoint
from gps_coordinate.config import WGS84_GPS, EPSG_32633_BALATON, EPSG_32634_BP


class TestGPSPoint(unittest.TestCase):

    def test_set_from_Xn_Yn(self):
        # Original point
        lat, lon = 46.949, 17.889  # Somewhere near Balaton
        gps = GPSPoint(lat, lon, crs_to=EPSG_32633_BALATON)

        # Convert to projected coordinates
        x = gps.Xn
        y = gps.Yn

        # Create new instance and set coordinates using projected values
        gps2 = GPSPoint(0, 0, crs_to=EPSG_32633_BALATON)  # Dummy init
        gps2.set_from_Xn_Yn(x, y)

        # Check if coordinates are restored correctly (allowing small numerical error)
        self.assertTrue(isclose(gps.latitude, gps2.latitude, abs_tol=1e-6))
        self.assertTrue(isclose(gps.longitude, gps2.longitude, abs_tol=1e-6))

    def test_set_from_Xn_Yn_custom_CRS(self):
        # Original point
        lat, lon = 46.949, 17.889  # Somewhere near Balaton
        gps = GPSPoint(lat, lon, crs_to=EPSG_32634_BP)

        # Convert to projected coordinates
        x = gps.Xn
        y = gps.Yn

        # Create new instance and set coordinates using projected values
        gps2 = GPSPoint(0, 0, crs_to=EPSG_32634_BP)  # Dummy init
        gps2.set_from_Xn_Yn(x, y)

        # Check if coordinates are restored WRONGLY (allowing small numerical error)
        self.assertTrue(isclose(gps.latitude, gps2.latitude, abs_tol=1e-6))
        self.assertTrue(isclose(gps.longitude, gps2.longitude, abs_tol=1e-6))

    def test_set_from_Xn_Yn_wrong_CRS(self):
        # Original point
        lat, lon = 46.949, 17.889  # Somewhere near Balaton
        gps = GPSPoint(lat, lon, EPSG_32633_BALATON)

        # Convert to projected coordinates
        x = gps.Xn
        y = gps.Yn

        # Create new instance and set coordinates using projected values
        gps2 = GPSPoint(0, 0, crs_to=EPSG_32634_BP)  # Dummy init
        gps2.set_from_Xn_Yn(x, y)

        # Check if coordinates are restored WRONGLY (allowing small numerical error)
        self.assertFalse(isclose(gps.latitude, gps2.latitude, abs_tol=1e-6))
        self.assertFalse(isclose(gps.longitude, gps2.longitude, abs_tol=1e-6))


if __name__ == "__main__":
    unittest.main()
