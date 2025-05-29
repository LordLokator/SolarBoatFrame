# from serial import Serial
import serial

port='/dev/ttyUSB0'
baudrate=115200
timeout=3

output = " "
ser = serial.Serial(
  port=port,
  baudrate=baudrate,
  timeout=timeout
)

while True:
  # print("----")
  output = ser.readline().decode("utf-8")
  print(output)
