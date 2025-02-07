import sys
import time

import digitalio
import busio
import board

from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,OV7670_COLOR_RGB,
    OV7670_TEST_PATTERN_COLOR_BAR_FADE,
)

# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus

#with digitalio.DigitalInOut(board.D39) as shutdown:
#    shutdown.switch_to_output(True)
#    time.sleep(0.001)
cam_bus = busio.I2C(scl=board.GP21, sda=board.GP20)

cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,#D0
        board.GP1,#D1
        board.GP2,#D2
        board.GP3,#D3
        board.GP4,#D4
        board.GP5,#D5
        board.GP6,#D6
        board.GP7,#D7
    ],
    clock=board.GP8,#PLK
    vsync=board.GP13,#VS
    href=board.GP12,#HS
    mclk=board.GP9,#XLK
    shutdown=board.GP15,#PWDN
    reset=board.GP14,#RET
)
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV  #OV7670_COLOR_RGB
#cam.flip_y = True

print(cam.width, cam.height)

buf = bytearray(2 * cam.width * cam.height)
print('##################################')
print(buf)
cam.capture(buf)
print('##################################')
print(len(buf))
print('##################################')
print(len(list(buf)))


chars =b"@#*+-:. "# b" .:-+*#"

width = cam.width
row = bytearray(2 * width)
while True:

    cam.capture(buf)
    for j in range(cam.height):
        for i in range(cam.width):
            row[i * 2] = row[i * 2 + 1] = chars[
                buf[2 * (width * j + i)] * (len(chars) - 1) // 255
            ]
        print(row)
    print()
    time.sleep(1.5)
