import can
from can.bus import BusState
from loguru import logger
import os
import threading

LOG_PATH = os.path.abspath(os.path.join("logging", "CAN_logs.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Kormány:
# init: kormány potméter állapot olvasás -> convert(x°) -> enum[], steppek (int vagy double)
# output már konvertákva menjen ki a CAN-re.

# Gázkar:
# kb ugyanaz, itt is diszkrétet választunk ki, konvertálunk, elküldjük CAN-en

# Start bit, UART: 0-255 gázkar (oszd el 2-vel)
# RUDDER-t, azaz irányt adunk meg, nem a hajó állását


# TODO: 1/10 - 1/20 küldjük ki az aktuális állást


ARBITRATION_ID_LOOKUP_TABLE = {
    'OUT_RUDDER': 0x200,
    'OUT_ENGINE': 0x201,

    'IN_VELOCITY_U_V_R': 0x100,
    'IN_RUDDER_ANGLE': 0x101,
    'IN_ENGINE_RPM': 0x102,
}


class CANManager:

    def __init__(
        self,
        channel: str = "default_channel",
        bitrate: int = 500000,
        interface: str = 'virtual',
    ):
        """
        Initialize the CAN manager.

        Args:
            channel (str, optional): Defaults to "default_channel".
            bitrate (int, optional): Defaults to 500000.
            interface (str, optional): Defaults to 'virtual'.
        """
        self.channel = channel
        self.bitrate = bitrate
        self.interface = interface

        self._lock = threading.Lock()
        self._state = {
            "u": 0.0,
            "v": 0.0,
            "r": 0.0,
            "rudder_angle": 0.0,
            "engine_rpm": 0.0
        }

        self.bus = can.interface.Bus(
            channel=self.channel,
            bitrate=self.bitrate,
            interface=self.interface
        )
        self._running = True
        self._recv_thread: threading.Thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._recv_thread.start()

    def _receive_loop(self):
        while self._running:
            msg = self._receive_message(timeout=1.0)
            if msg:
                self._handle_message(msg)

    def _handle_message(self, msg: can.Message):
        with self._lock:

            try:
                # TODO: Placeholder
                if msg.arbitration_id == ARBITRATION_ID_LOOKUP_TABLE['IN_VELOCITY_U_V_R']:  # velocity info
                    self._state["u"] = msg.data[0] / 10
                    self._state["v"] = msg.data[1] / 10
                    self._state["r"] = msg.data[2] / 10

                elif msg.arbitration_id == ARBITRATION_ID_LOOKUP_TABLE['IN_RUDDER_ANGLE']:  # rudder
                    self._state["rudder_angle"] = msg.data[0] / 10

                elif msg.arbitration_id == ARBITRATION_ID_LOOKUP_TABLE['IN_ENGINE_RPM']:  # engine
                    self._state["engine_rpm"] = int.from_bytes(msg.data[0:2], "big")

                logger.debug(f"Updated CAN state from ID 0x{msg.arbitration_id:X}")

            except Exception as e:
                logger.error(f"Failed to parse CAN message: {e}")

    def read_state(self) -> dict:
        with self._lock:
            return self._state.copy()

    def send_control(self, rudder: float, rpm: float):
        rudder_data = bytes([int(rudder * 10)])
        rpm_data = int(rpm).to_bytes(2, "big")

        # TODO: sanity checking here
        self.send_message(arbitration_id=ARBITRATION_ID_LOOKUP_TABLE['OUT_RUDDER'], data=rudder_data)
        self.send_message(arbitration_id=ARBITRATION_ID_LOOKUP_TABLE['OUT_ENGINE'], data=rpm_data)

    def send_message(self, arbitration_id: int, data: bytes):
        """Send a CAN message."""
        if not self.bus:
            raise can.exceptions.CanOperationError(f"Bus was not initiated!")

        message = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=False
        )
        try:
            self.bus.send(message)
            print(f"Message sent: {message}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def _receive_message(self, timeout: float = 1.0):
        """Receive a CAN message with an optional timeout."""
        if not self.bus:
            raise can.exceptions.CanOperationError(f"Bus was not initiated!")

        message = self.bus.recv(timeout=timeout)
        if message:
            logger.debug(f"Message received: {message}")
        else:
            logger.debug("No message received within the timeout.")
        return message

    def shutdown(self):
        self._running = False
        self._recv_thread.join()
        self.bus.shutdown()

        if not self._recv_thread.is_alive() \
                and self.bus.state != BusState.ACTIVE \
                and self.bus.state != BusState.ERROR:
            logger.info("CANManager shut down.")
        else:
            _stats = f"BusState: {self.bus.state} | recv thread isalive: {self._recv_thread.is_alive()}"
            logger.warning(f"CANManager shutdown anomaly! {_stats}")


if __name__ == "__main__":
    can_manager = CANManager(
        channel="vcan0",
        interface='virtual',
        bitrate=500000
    )
    # testing main, notice 'virtual'.

    PAYLOAD: list[int] = [k for k in range(5)]
    can_manager.send_message(arbitration_id=0x123, data=PAYLOAD)
    can_manager._receive_message(timeout=2.0)  # not sure if this works because of race condition!
    print(can_manager._state)
