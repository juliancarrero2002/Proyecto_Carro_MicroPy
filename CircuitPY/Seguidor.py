import sys
import time
import pwmio
import digitalio
import busio
import board

vel_ini_derecha = 55
vel_ini_izquierda = 55

# Comunicación UART
uart = busio.UART(board.GP16, board.GP17, baudrate=9600)

# Configuración PWM para motores
pwm_derecha = pwmio.PWMOut(board.GP20, frequency=100000, duty_cycle=0)
pwm_izquierda = pwmio.PWMOut(board.GP21, frequency=100000, duty_cycle=0)

# NUEVA CONFIGURACIÓN PARA MOTOR EN GP10 Y GP11
pwm_motor2_a = pwmio.PWMOut(board.GP10, frequency=100000, duty_cycle=0)
pwm_motor2_b = pwmio.PWMOut(board.GP11, frequency=100000, duty_cycle=0)

pwm_derecha.duty_cycle = 0
pwm_izquierda.duty_cycle = 0
pwm_motor2_a.duty_cycle = 0
pwm_motor2_b.duty_cycle = 0

from adafruit_ov7670 import (
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
    OV7670_TEST_PATTERN_COLOR_BAR_FADE,
)

# Configuración de la cámara
cam_bus = busio.I2C(board.GP19, board.GP18)

cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0, board.GP1, board.GP2, board.GP3,
        board.GP4, board.GP5, board.GP6, board.GP7,
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

buf = bytearray(2 * cam.width * cam.height)

width = cam.width
row = bytearray(2 * width)

while True:
    cam.capture(buf)
    
    matrix = []
    rw = []
    for i in range(cam.width):
        intensity = "0" if buf[2 * (width * (cam.height - 1) + i)] * 10 // 255 < 5 else "-"
        rw.append(intensity)
    
    matrix.append(rw)

    ulinea = matrix[len(matrix)-1][:]
    suma = 0
    contador = 0
    for i in range(len(ulinea)):
        suma += i if ulinea[i] == "0" else 0
        contador += 1 if ulinea[i] == "0" else 0
    promedio = suma / contador if contador != 0 else 0
    
    diferencia = (20 - promedio) * (100 / 20) if promedio != 0 else 100
    if promedio != 0:
        if diferencia < 0:
            pwm_derecha.duty_cycle = int(((vel_ini_derecha / 100) * 65535) * (1 - abs((diferencia) / 100) * 0.8))
            pwm_izquierda.duty_cycle = int((vel_ini_izquierda / 100) * 65535)
            
            # Ajuste para el segundo motor
            pwm_motor2_a.duty_cycle = pwm_derecha.duty_cycle
            pwm_motor2_b.duty_cycle = 0  # Motor en dirección A
            
        else:
            pwm_izquierda.duty_cycle = int(((vel_ini_izquierda / 100) * 65535) * (1 - abs((diferencia) / 100) * 0.8))
            pwm_derecha.duty_cycle = int((vel_ini_derecha / 100) * 65535)
            
            # Ajuste para el segundo motor
            pwm_motor2_a.duty_cycle = 0  # Motor en dirección B
            pwm_motor2_b.duty_cycle = pwm_izquierda.duty_cycle
            
    else:
        pwm_derecha.duty_cycle = 0
        pwm_izquierda.duty_cycle = 0
        pwm_motor2_a.duty_cycle = 0
        pwm_motor2_b.duty_cycle = 0
    
    time.sleep(0.08)
    
    pwm_derecha.duty_cycle = 65535
    pwm_izquierda.duty_cycle = 65535
    pwm_motor2_a.duty_cycle = 65535
    pwm_motor2_b.duty_cycle = 0  # Mantener dirección A
