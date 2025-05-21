from abc import ABC, abstractmethod
from ..base import GPSPoint


class Geofence(ABC):
    @abstractmethod
    def contains(self, point: GPSPoint) -> bool:
        pass

    def __contains__(self, point: GPSPoint) -> bool:
        return self.contains(point)
