import time
import board
import digitalio
import pwmio
from digitalio import DigitalInOut, Direction

# Configuración de los pines del motor A y B
Motor_A_Adelante = DigitalInOut(board.GP16)
Motor_A_Atras = DigitalInOut(board.GP17)
Motor_B_Adelante = DigitalInOut(board.GP22)
Motor_B_Atras = DigitalInOut(board.GP26)

# Configuración de los pines de habilitación (PWM)
Enable_A = pwmio.PWMOut(board.GP10, frequency=1000, duty_cycle=65535)  # Máxima velocidad
Enable_B = pwmio.PWMOut(board.GP11, frequency=1000, duty_cycle=65535)  # Máxima velocidad

# Configuración de los pines para sensores IR como ENTRADAS
right_ir = DigitalInOut(board.GP18)  # Sensor IR derecho
right_ir.direction = Direction.INPUT
left_ir = DigitalInOut(board.GP19)   # Sensor IR izquierdo
left_ir.direction = Direction.INPUT

# Mover hacia adelante
def move_forward():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = True  # Motor A hacia adelante
    Motor_A_Atras.value = False     # Detener Motor A hacia atrás
    Motor_B_Adelante.value = True   # Motor B hacia adelante
    Motor_B_Atras.value = False     # Detener Motor B hacia atrás

# Mover hacia atrás
def move_backward():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = False   # Detener Motor A hacia adelante
    Motor_A_Atras.value = True       # Motor A hacia atrás
    Motor_B_Adelante.value = False    # Detener Motor B hacia adelante
    Motor_B_Atras.value = True        # Motor B hacia atrás

# Girar a la derecha (Motor A avanza, Motor B se detiene)
def turn_right():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = True     # Motor A avanza
    Motor_A_Atras.value = False        # Detener Motor A hacia atrás
    Motor_B_Adelante.value = False     # Detener Motor B
    Motor_B_Atras.value = False        # Detener Motor B
    time.sleep(0.5)                    # Mantener el giro por un tiempo
    stop()

# Girar a la izquierda (Motor B avanza, Motor A se detiene)
def turn_left():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = False    # Detener Motor A hacia adelante
    Motor_A_Atras.value = False        # Detener Motor A hacia atrás
    Motor_B_Adelante.value = True      # Motor B avanza
    Motor_B_Atras.value = False        # Detener Motor B hacia atrás
    time.sleep(0.5)                    # Mantener el giro por un tiempo
    stop()

# Detener ambos motores
def stop():
    Motor_A_Adelante.value = False     # Detener Motor A hacia adelante
    Motor_A_Atras.value = False         # Detener Motor A hacia atrás
    Motor_B_Adelante.value = False      # Detener Motor B hacia adelante
    Motor_B_Atras.value = False         # Detener Motor B hacia atrás

while True:
    right_val = right_ir.value  # Leer valor del sensor IR derecho
    left_val = left_ir.value    # Leer valor del sensor IR izquierdo

    print(str(right_val) + "-" + str(left_val))

    # Establecer condiciones para la evitación de obstáculos
    if right_val == False and left_val == False:
        move_forward()
    elif right_val == True and left_val == False:
        turn_right()
    elif right_val == False and left_val == True:
        turn_left()
    else:
        stop()