# main.py
# Entry point

from datetime import datetime
import time
from loguru import logger

from can_bus.can_manager import CANManager
from ship_manager import ShipManager


def main():
    logger.info(f"Starting application at {datetime.now()}")

    waittime = 0.2

    ship_manager = ShipManager()
    can_manager = CANManager(
        # channel=...,
        # bitrate=...,
        # bustype=...,
        # interface=...,
    )

    # TODO: while any task is ongoing instead of True
    # TODO: safeguards?...
    while True:
        ship_manager.step()

        # Minden, ami a következő GPS koordináta megszülését jelenti,
        # a ship_manager-ben történik!
        next_objective = ship_manager.get_next_objective_coo()

        # TODO: Kitaláljuk, mit mondjunk az aktuárotorknak
        ...

        # TODO: a CAN üzeneteit majd valahogy be kell vezetni a manager-be!
        # e.g rudder state

        # TODO: Közvetítünk a CAN felé.
        can_manager.send_message(
            # tell engine to do stuff...
        )

        can_manager.send_message(
            # tell rudder to do stuff...
        )

        # Valamilyen FPS-el futtatjuk ezeket a függvényeket:
        time.sleep(waittime)
