import os
from threading import Lock
from loguru import logger
from .base import GPSPoint

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    rotation="500 KB",
    backtrace=True,
    diagnose=True
)


class ShipPosition(GPSPoint):
    _instance = None
    _singleton_lock = Lock()
    _lock = Lock()

    def __new__(cls, latitude=0.0, longitude=0.0):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, latitude=0.0, longitude=0.0):

        # Ha nem létezik a '__initialized' attributum, hamisnak vesszük;
        if not getattr(self, '__initialized', False):
            super().__init__(latitude, longitude)

            # '"__initialized" is not accessed' ->
            # A 'getattr' igenis eléri, csak ezt a linter nem tudja szegény
            self.__initialized = True

    def update_position(self, new_lat, new_lon):
        self.set_coordinates(new_lat, new_lon)
