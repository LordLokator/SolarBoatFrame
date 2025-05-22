# objective.py

import os
from loguru import logger
from typing import Optional
from .base import GPSPoint

# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "coordinates.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    backtrace=True,
    diagnose=True
)


class ObjectiveCoordinate(GPSPoint):
    """
    Represents a navigation goal or checkpoint.
    """

    def __init__(self, latitude: float, longitude: float, label: Optional[str] = None):
        super().__init__(latitude, longitude)
        self.label = label or "Unnamed Objective"

        msg = f"Initialized ObjectivePoint: {self.label} at ({self.latitude}, {self.longitude})"
        logger.debug(msg)

    def __repr__(self):
        return f"ObjectivePoint(label={self.label}, lat={self.latitude}, lon={self.longitude})"
