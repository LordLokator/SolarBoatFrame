"""Ide kellenek a statikus tulajdonságok, pl hajó merülése, vagy közvetlenül ebből származtatott mennyiségek."""


class ShipProperties:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # TODO
        ...
