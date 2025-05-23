# ship_state/ship_properties.py
"""Ide kellenek a statikus tulajdonságok, pl hajó merülése, vagy közvetlenül ebből származtatott mennyiségek."""


from dataclasses import dataclass
import os
from textwrap import dedent  # removes unneded space from the beginning of strings.
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

    def __post_init__(self):
        logger.warning("This is the Blue Lady's config for testing purposes!")
        logger.debug(dedent(
            f"""{type(self).__name__} object, params: \n | length: {self.length} \n | breadth: {self.breadth} \n | draft: {self.draft} \n | displacement: {self.displacement} \n | x_g: {self.x_g}"""
        ))


@dataclass(frozen=True)
class LanaShipProperties:
    # TODO: write Lana's config here

    length:         float = 13.78   # LOA
    breadth:        float = 2.38    # B
    draft:          float = 0.86    # Td
    displacement:   float = 22.83   # Delta
    x_g:            float = 0.0     # center of gravity x position (usually 0)

    def __post_init__(self):
        logger.info("Using Lana's config.")
        logger.debug(dedent(
            f"""{type(self).__name__} object, params: \n | length: {self.length} \n | breadth: {self.breadth} \n | draft: {self.draft} \n | displacement: {self.displacement} \n | x_g: {self.x_g}"""
        ))
