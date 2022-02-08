from serial import Serial
import time

# connecting to the arduino
# on my windows
# display = Serial(port='COM3', baudrate=9600, timeout=.1)
# on my mac
display = Serial('/dev/tty.usbmodem141201')  # open serial port
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
