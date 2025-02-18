import can


class CANManager:

    def __init__(
        self,
        channel: str = "default_channel",
        bustype: str = "socketcan",
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
        self.bustype = bustype
        self.bitrate = bitrate
        self.interface = interface

        self.bus = can.interface.Bus(
            channel=self.channel,
            bustype=self.bustype,
            bitrate=self.bitrate,
            interface=self.interface
        )

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
            print(f"Message sent: {message}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def receive_message(self, timeout: float = 1.0):
        """
        Receive a CAN message with an optional timeout.
        """
        if not self.bus:
            raise can.exceptions.CanOperationError(f"Bus was not initiated!")

        message = self.bus.recv(timeout=timeout)
        if message:
            print(f"Message received: {message}")
        else:
            print("No message received within the timeout.")
        return message

    def shutdown(self):
        """
        Shutdown the CAN manager and clean up resources.
        """
        if self.bus:
            self.bus.shutdown()
            print("CAN bus shut down.")


if __name__ == "__main__":
    can_manager = CANManager(
        channel="vcan0",
        bustype="socketcan",
        bitrate=500000
    )
    PAYLOAD: list[int] = [k for k in range(5)]
    can_manager.send_message(arbitration_id=0x123, data=PAYLOAD)
    can_manager.receive_message(timeout=2.0)
    can_manager
