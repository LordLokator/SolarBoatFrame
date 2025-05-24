# Placeholder class.

from loguru import logger
from .net_helper import get_local_ip


class LTEManager:
    def __init__(self):
        self.ip_addr = get_local_ip()

        raise NotImplementedError()

    def connect(self) -> None:
        # Establish PPP or check SIM/registration
        raise NotImplementedError()

    def get_signal_quality(self) -> float:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()
