"""Writes this PC's IP to an ini file."""

from configparser import ConfigParser
from datetime import datetime
import socket
import os
from loguru import logger


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip, _ = s.getsockname()
    finally:
        s.close()
    return local_ip



if __name__ == "__main__":
    # Setup logging
    LOG_PATH = os.path.abspath(os.path.join("logging", "networking.log"))

    logger.add(
        LOG_PATH,
        level="DEBUG",
        backtrace=True,
        diagnose=True
    )

    fp = 'net_config.ini'
    config = ConfigParser()

    # Read existing config if it exists
    if os.path.exists(fp):
        config.read(fp)

    read_ip_address = get_local_ip()

    logger.info(f"The IP of this machine is [{read_ip_address}] [At: {datetime.now()}].")

    # Overwrite only the 'Networking' section
    config['Networking'] = {
        'imagezmq_ip': read_ip_address,
    }

    # Save back, preserving all other sections
    with open(fp, 'w') as configfile:
        config.write(configfile)
