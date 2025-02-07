import board
import busio
import digitalio
import pwmio
import random
import time
from adafruit_ov7670 import OV7670, OV7670_SIZE_DIV16, OV7670_COLOR_YUV

# Configuración de los pines del carrito
m11 = digitalio.DigitalInOut(board.GP16)
m11.direction = digitalio.Direction.OUTPUT
m12 = digitalio.DigitalInOut(board.GP17)
m12.direction = digitalio.Direction.OUTPUT
m21 = digitalio.DigitalInOut(board.GP10)
m21.direction = digitalio.Direction.OUTPUT
m22 = digitalio.DigitalInOut(board.GP11)
m22.direction = digitalio.Direction.OUTPUT

# Configuración de PWM para controlar la velocidad de los motores
pwm_izquierdo = pwmio.PWMOut(board.GP22, frequency=1000, duty_cycle=0)  # ENA
pwm_derecho = pwmio.PWMOut(board.GP21, frequency=1000, duty_cycle=0)   # ENB

# Configuración de la cámara
cam_bus = busio.I2C(board.GP19, board.GP18)
cam = OV7670(
    cam_bus,
    data_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7],
    clock=board.GP9,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP8,
    shutdown=board.GP15,
    reset=board.GP14,
)

cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV

# Funciones de control del carrito
def detener_carrito():
    m11.value = False
    m12.value = False
    m21.value = False
    m22.value = False
    pwm_izquierdo.duty_cycle = 0
    pwm_derecho.duty_cycle = 0

def mover_adelante(speed=32768):
    m11.value = True
    m12.value = False
    m21.value = True
    m22.value = False
    pwm_izquierdo.duty_cycle = speed
    pwm_derecho.duty_cycle = speed

def mover_atras(speed=32768):
    m11.value = False
    m12.value = True
    m21.value = False
    m22.value = True
    pwm_izquierdo.duty_cycle = speed
    pwm_derecho.duty_cycle = speed

def girar_izquierda(speed=32768):
    m11.value = True
    m12.value = False
    m21.value = False
    m22.value = False
    pwm_izquierdo.duty_cycle = speed
    pwm_derecho.duty_cycle = speed

def girar_derecha(speed=32768):
    m11.value = False
    m12.value = False
    m21.value = True
    m22.value = False
    pwm_izquierdo.duty_cycle = speed
    pwm_derecho.duty_cycle = speed

# Búfer para capturar imágenes de la cámara
buf = bytearray(2 * cam.width * cam.height)

while True:
    cam.capture(buf)
    matrix = []
    for j in range(cam.height):
        row = []
        for i in range(cam.width):
            intensity = "0" if (buf[2 * (cam.width * j + i)] * 10 // 255) < 5 else "-"
            row.append(intensity)
        matrix.append(row)

    ulinea = matrix[-1]
    suma = sum(i for i, val in enumerate(ulinea) if val == "0")
    contador = sum(1 for val in ulinea if val == "0")

    promedio = suma / contador if contador != 0 else 0
    diferencia = (20 - promedio) * (100 / 20) if promedio != 0 else 100
    diferencia = (diferencia / 2) + 50

    speed_izq = random.randint(20000, 60000)
    speed_der = random.randint(20000, 60000)

    if diferencia > 60:
        girar_derecha(speed_der)
    elif diferencia < 40:
        girar_izquierda(speed_izq)
    else:
        mover_adelante((speed_izq + speed_der) // 2)

    time.sleep(0.01)
