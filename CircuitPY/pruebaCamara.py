import time
import busio
import board
from adafruit_ov7670 import OV7670, OV7670_SIZE_DIV16, OV7670_COLOR_RGB

# Configuración de la cámara
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

cam = OV7670(
    i2c,
    data_pins=[
        board.GP0,  # D0
        board.GP1,  # D1
        board.GP2,  # D2
        board.GP3,  # D3
        board.GP4,  # D4
        board.GP5,  # D5
        board.GP6,  # D6
        board.GP7,  # D7
    ],
    clock=board.GP8,      # PCLK
    vsync=board.GP13,     # VSYNC
    href=board.GP12,      # HREF
    mclk=board.GP9,       # MCLK
    shutdown=board.GP15,  # PWDN
    reset=board.GP14      # RESET
)

# Configura tamaño de la imagen y colores
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_RGB

# Captura de prueba
print("Iniciando prueba de captura...")

# Crear un buffer
buf = bytearray(2 * cam.width * cam.height)

try:
    cam.capture(buf)
    print("Captura exitosa. Tamaño del buffer:", len(buf))
except Exception as e:
    print("Error al capturar imagen:", e)

