# main.py
# Entry point

from datetime import datetime
from loguru import logger

from ship_manager import ShipManager


def main():
    logger.info(f"Starting application at {datetime.now()}")

    ship_manager = ShipManager()

