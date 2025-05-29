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
class ShipProperties:
    length:         float = 0.0  # LOA
    breadth:        float = 0.0  # B
    draft:          float = 0.0  # Td
    displacement:   float = 0.0  # Delta
    x_g:            float = 0.0  # center of gravity x position (usually 0)
    

    def __post_init__(self):
        logger.warning("This is an Empty config for testing purposes!")
        logger.debug(dedent(
            f"""{type(self).__name__} object, params: \
                    | length: {self.length} \
                    | breadth: {self.breadth} \
                    | draft: {self.draft} \
                    | displacement: {self.displacement} \
                    | x_g: {self.x_g}"""
        ))


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
            f"""{type(self).__name__} object, params: \
                    | length: {self.length} \
                    | breadth: {self.breadth} \
                    | draft: {self.draft} \
                    | displacement: {self.displacement} \
                    | x_g: {self.x_g}"""
        ))
        


@dataclass(frozen=True)
class LanaShipProperties:
    # TODO: write Lana's config here

    length:         float = 13.78   # LOA
    breadth:        float = 2.38    # B
    draft:          float = 0.86    # Td
    displacement:   float = 22.83   # Delta
    x_g:            float = 0.0     # center of gravity x position (usually 0)

    # Values of parameters describing the approximation of the ahead distance for starting the turning maneuver
    a6 = 5.987527e-09
    a5 = -1.561371e-06
    a4 = 1.430259e-04
    a3 = -0.004935727
    a2 = 0.01235089
    a1 = 2.10745127
    a0 = -0.02348713
    
    #parameters of the propeller/rudder control system
    kTp = 4.5658 
    kTn = 3.2903 
    kyT = - 0.1333    
    knT = - 0.2024    
    kyL = 1.1760    
    knL = - 0.5493    
    LxR = 5.7800   
    kFp = 272.1
    kFn = 204.1
    k1 = 0.3850
    k2 = 0.3000
    k3 = 0.4900
    k4 = 0.0217
    k5 = 0.1150
    
    def __post_init__(self):
        logger.info("Using Lana's config.")
        logger.debug(dedent(
            f"""{type(self).__name__} object, params: \
                    | length: {self.length} \
                    | breadth: {self.breadth} \
                    | draft: {self.draft} \
                    | displacement: {self.displacement} \
                    | x_g: {self.x_g}"""
        ))
