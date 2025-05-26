class MockGPSManager:
    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon

    def get_live_location(self):
        return self._lat, self._lon

    def set_mock_location(self, lat, lon):
        self._lat = lat
        self._lon = lon
