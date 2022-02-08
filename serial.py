import serial
import time

# windows
display = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

print(display.name)
display.write(b'Hello')

while True:
    print(display.readline())
    time.sleep(.5)
