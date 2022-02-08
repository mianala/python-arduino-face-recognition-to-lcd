from serial import Serial
import time

# windows
display = Serial(port='COM3', baudrate=9600, timeout=.1)

print(display.name)
display.write(b'Hello')

# while True:
#     print(display.readline())
#     display.write(b'Hello')

#     time.sleep(2)
