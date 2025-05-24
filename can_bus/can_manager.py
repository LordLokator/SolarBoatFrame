import can
from loguru import logger
import os
import threading
import time

LOG_PATH = os.path.abspath(os.path.join("logging", "CAN_logs.log"))

logger.add(
    LOG_PATH,
    level="DEBUG",
    rotation="500 KB",
    backtrace=True,
    diagnose=True
)


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
            bustype (str, optional): Defaults to "socketcan".
            bitrate (int, optional): Defaults to 500000.
            interface (str, optional): Defaults to 'virtual'.
        """
        self.channel = channel
        self.bitrate = bitrate
        self.interface = interface

        self.bus = can.interface.Bus(
            channel=self.channel,
            bitrate=self.bitrate,
            interface=self.interface
        )
    
    def listen_loop(self):
        """
        Continuously listens to the CAN bus in a separate thread.
        """
        logger.info(f"Listening started in thread: {threading.current_thread().name}")
        while True:
            try:
                message = self.receive_message(timeout=1.0)
                if message:
                    logger.info(f"Message received: {message}")
            except Exception as e:
                logger.error(f"Error in listen_loop: {e}")
            time.sleep(0.1)

    def send_message(self, arbitration_id: int, data: bytes):
        """
        Send a CAN message.
        """
        if not self.bus:
            raise can.exceptions.CanOperationError(f"Bus was not initiated!")

        message = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=False
        )
        try:
            self.bus.send(message)
            logger.success(f"Message sent: {message}")
        except can.CanError as e:
            logger.error(f"Failed to send message: {e}")

    def receive_message(self, timeout: float = 1.0):
        """
        Receive a CAN message with an optional timeout.
        """
        if not self.bus:
            raise can.exceptions.CanOperationError(f"Bus was not initiated!")

        message = self.bus.recv(timeout=timeout)
        if message:
            logger.debug(f"Received message: {message}")
        else:
            logger.warning("No message received within the timeout.")
        return message

    def shutdown(self):
        """
        Shutdown the CAN manager and clean up resources.
        """
        if self.bus:
            self.bus.shutdown()
            logger.info("CAN bus shut down.")


if __name__ == "__main__":
    can_manager = CANManager(
        channel="vcan0",
        bitrate=500000
    )

    try:
        PAYLOAD: list[int] = [k for k in range(5)]
        can_manager.send_message(arbitration_id=0x123, data=bytes(PAYLOAD))
    except can.exceptions.CanOperationError as e:
        logger.error(f"CAN operation failed: {e}")

    try:
        can_manager.receive_message()
    except can.exceptions.CanOperationError as e:
        logger.error(f"CAN operation failed: {e}")

    listener_thread = threading.Thread(
        target=can_manager.listen_loop,
        name="CANListenerThread",
        daemon=True
    )
    listener_thread.start()


    time.sleep(10)

    can_manager.shutdown()
