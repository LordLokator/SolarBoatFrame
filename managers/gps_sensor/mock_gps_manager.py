class MockGPSManager:
    def __init__(self, lat, lon, heading):
        self._lat = lat
        self._lon = lon
        self._heading = heading

    def get_live_location(self):
        return self._lat, self._lon, self._heading

    def set_mock_location(self, lat, lon, heading):
        self._lat = lat
        self._lon = lon
        self._heading = heading
