# ship_state/ship_properties.py
"""Ide kellenek a statikus tulajdonságok, pl hajó merülése, vagy közvetlenül ebből származtatott mennyiségek."""


from dataclasses import dataclass


@dataclass
class ShipProperties:
    length: float  # LOA
    breadth: float  # B
    draft: float  # Td
    displacement: float  # Delta
    x_g: float  # center of gravity x position (usually 0)
