import board
import busio
import random
import time

import pwmio
import digitalio
from adafruit_ov7670 import (OV7670, OV7670_SIZE_DIV16, OV7670_COLOR_YUV)

# Configuración de los pines del carrito
m11 = digitalio.DigitalInOut(board.GP16)
m11.direction = digitalio.Direction.OUTPUT
m12 = digitalio.DigitalInOut(board.GP17)
m12.direction = digitalio.Direction.OUTPUT
m21 = digitalio.DigitalInOut(board.GP10)
m21.direction = digitalio.Direction.OUTPUT
m22 = digitalio.DigitalInOut(board.GP11)
m22.direction = digitalio.Direction.OUTPUT

# Configuración de la cámara
cam_bus = busio.I2C(board.GP19, board.GP18)
cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP9,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP8,
    shutdown=board.GP15,
    reset=board.GP14,
)

cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = False

# Configuración de PWM para controlar la velocidad del carrito
pwm = pwmio.PWMOut(board.GP22, frequency=100, duty_cycle=0)

# Funciones de control del carrito
def detener_carrito():
    m11.value = False
    m12.value = False
    m21.value = False
    m22.value = False

def mover_adelante():
    m11.value = True
    m12.value = False
    m21.value = True
    m22.value = False

def mover_atras():
    m11.value = False
    m12.value = True
    m21.value = False
    m22.value = True

def girar_izquierda():
    m11.value = True
    m12.value = False
    m21.value = False
    m22.value = False

def girar_derecha():
    m11.value = False
    m12.value = False
    m21.value = True
    m22.value = False

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
            print(intensity, end=' ')
        matrix.append(row)
        print()
    print()

    aplanado = [elemento for fila in matrix for elemento in fila]

    # Procesar la última línea de la imagen para determinar la dirección
    ulinea = matrix[-1][:]
    suma = 0
    contador = 0
    for i in range(len(ulinea)):
        if ulinea[i] == "0":
            suma += i
            contador += 1

    promedio = suma / contador if contador != 0 else 0
    diferencia = (20 - promedio) * (100 / 20) if promedio != 0 else 100
    diferencia = (diferencia / 2) + 50

    print(f'Diferencia: {diferencia}')

    if diferencia > 60:
        girar_derecha()
        speed_1 = random.randint(20, 120)
        ruedader = 0
        print(f"Rueda derecha: {ruedader}, Rueda izq: {speed_1}")

    elif diferencia < 40:
        girar_izquierda()
        speed_2 = random.randint(20, 120)
        ruedaizq = 0
        print(f"Rueda derecha: {speed_2}, Rueda izq: {ruedaizq}")

    else:
        mover_adelante()
        speed_2 = random.randint(20, 120)
        print(f"Rueda derecha: {speed_2}, Rueda izq: {speed_2}")

    time.sleep(0.01)
