import threading
import serial

class SerialParamReader:
    def __init__(self, port='/dev/ttyACM0', baudrate=115_200, timeout=2):
        self.serial_port = serial.Serial(port, baudrate, timeout=timeout)
        self.param1 = None
        self.param2 = None
        self.default_param1 = 0
        self.default_param2 = 0
        self._lock = threading.Lock()

    def set_params(self, param1, param2):
        with self._lock:
            self.param1 = param1
            self.param2 = param2

    def read_input(self):
        if not self.serial_port.is_open:
            self.serial_port.open()

        try:
            line = self.serial_port.readline().decode('utf-8').strip()
            if line == '0':
                return self.default_param1, self.default_param2

            elif line == '1':
                with self._lock:
                    if self.param1 is not None and self.param2 is not None:
                        return (self.param1, self.param2)

                    else:
                        raise ValueError("Parameters not set yet.")
            else:
                raise ValueError(f"Unexpected input: {line}")
        except Exception as e:
            print(f"[Error] {e}")
            return None

    def send_reply(self, msg):
        self.serial_port.write(bytearray(msg,'utf-8'))

if __name__ == '__main__':
    reader = SerialParamReader()
    reader.set_params(42, 99)

    i = 1
    signal = False
    while True:
        print("sending...")
        reader.send_reply("1" if signal else "0")
        rpl = reader.read_input()
        print(rpl)
        if i%10 == 0:
            signal = not signal
        i+=1