import os
import time
from serial import Serial
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL
from loguru import logger


# Setup logging
LOG_PATH = os.path.abspath(os.path.join("logging", "gps_manager.log"))


class GPSManager:
    def __init__(self, port='/dev/ttyUSB0', baudrate=38400, timeout=3):
        # NOTE: 'ttyUSB0' is used.
        # If this doesn't work, consider the following:
        # In console, list every USB device: ' ls /dev/tty '
        #     tty is the terminal associated with the current process
        #     tty1-tty63 are virtual consoles
        #     ttyACM* -> 'generic USB class driver for a modem, but works for serial devices with no modem'
        #     ttyUSB* -> 'have chipset-specific drivers in the Linux kernel'

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.stream = None
        self.ubr = None
        self._initialize()

        # WARMUP! NEEDED FOR MORE CONSISTENT STARTUP!
        _, _ = self.get_live_location(timeout=5)

    def _initialize(self):
        try:
            self.stream = Serial(self.port, self.baudrate, timeout=self.timeout)
            self.ubr = UBXReader(self.stream, protfilter=NMEA_PROTOCOL | UBX_PROTOCOL)
            logger.debug("Serial connection and UBXReader initialized.")

        except Exception as e:
            logger.exception("Failed to initialize GPSManager: {}", e)

    def get_live_location(self, timeout: float = 2.0, interval: float = 0.2) -> tuple[float, float]:
        """Asynchronously attempt to get a valid GPS reading for up to ~2 seconds. Order: lat - lon.

        Args:
            timeout (float): Max seconds to wait for a valid reading.
            interval (float): Time between polls.

        Returns:
            tuple[float, float]: Latitude - Longitude
        """

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                raw_data, parsed_data = self.ubr.read()
                if parsed_data is not None and hasattr(parsed_data, 'lat') and hasattr(parsed_data, 'lon'):
                    logger.debug("Location received: lat={}, lon={}", parsed_data.lat, parsed_data.lon)
                    return parsed_data.lat, parsed_data.lon

                logger.debug("Waiting for GPS fix...")

            except Exception as e:
                logger.exception("Error while reading location: {}", e)

            time.sleep(interval)

        logger.warning("GPS fix not acquired within timeout.")
        return None, None

    def close(self):
        if self.stream:
            self.stream.close()
            logger.debug("Serial stream closed.")
