from serial import Serial
import time

# windows
# connecting to the arduino
display = Serial(port='COM3', baudrate=9600, timeout=.1)

print(display.name)
time.sleep(4)

display.write(b'Hello')
time.sleep(4)

display.write(b'Mianala')
time.sleep(4)

display.write(b'Mandeha')
# while True:
#     print(display.readline())
#     display.write(b'Hello')

#     time.sleep(2)
