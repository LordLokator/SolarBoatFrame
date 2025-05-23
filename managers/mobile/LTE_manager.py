# Placeholder class.

class LTEManager:
    def __init__(self):
        raise NotImplementedError()

    def connect(self) -> None:
        # Establish PPP or check SIM/registration

        raise NotImplementedError()

    def get_signal_quality(self) -> float:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()
