# ship/ship_properties.py
"""Ide kellenek a statikus tulajdonságok, pl hajó merülése, vagy közvetlenül ebből származtatott mennyiségek."""


from dataclasses import dataclass
import os
from loguru import logger

LOG_PATH = os.path.abspath(os.path.join("logging", "ship_state.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    backtrace=True,
    diagnose=True
)


@dataclass(frozen=True)
class BlueLadyShipProperties:

    length:         float = 13.78   # LOA
    breadth:        float = 2.38    # B
    draft:          float = 0.86    # Td
    displacement:   float = 22.83   # Delta
    x_g:            float = 0.0     # center of gravity x position (usually 0)

    # inertia_z:      float = 436_830.2
    # mass:           float = 22_934.4
    # X_u_dot:        float = -730.5
    # Y_v_dot:        float = -18_961.8
    # N_r_dot:        float = -183_519.1

    max_rudder_deg: float = 35.0   # Rudder maximum, in degrees

    def __post_init__(self):
        logger.warning("This is the Blue Lady's config for testing purposes!")
        logger.debug(
            f"""{type(self).__name__} object, params: \n | length: {self.length} \n | breadth: {self.breadth} \n | draft: {self.draft} \n | displacement: {self.displacement} \n | x_g: {self.x_g}"""
        )


@dataclass(frozen=True)
class LanaShipProperties:
    # TODO: write Lana's config here

    length:         float = 13.78   # LOA
    breadth:        float = 2.38    # B
    draft:          float = 0.86    # Td
    displacement:   float = 22.83   # Delta
    x_g:            float = 0.0     # center of gravity x position (usually 0)

    # inertia_z:      float = 436_830.2
    # mass:           float = 22_934.4
    # X_u_dot:        float = -730.5
    # Y_v_dot:        float = -18_961.8
    # N_r_dot:        float = -183_519.1

    max_rudder_deg: float = 35.0   # Rudder maximum, in degrees

    def __post_init__(self):
        logger.info("Using Lana's config.")
        logger.debug(
            f"""{type(self).__name__} object, params: \n | length: {self.length} \n | breadth: {self.breadth} \n | draft: {self.draft} \n | displacement: {self.displacement} \n | x_g: {self.x_g}"""
        )
