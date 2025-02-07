import wifi
import socketpool
import microcontroller
import time
import board
import pwmio
from digitalio import DigitalInOut, Direction

ssid = 'Carrero Ariza'
password = 'Juseca7216'

# Definir pines de control para el puente H
Motor_A_Adelante = DigitalInOut(board.GP16)
Motor_A_Atras = DigitalInOut(board.GP17)
Motor_B_Adelante = DigitalInOut(board.GP10)
Motor_B_Atras = DigitalInOut(board.GP11)
Motor_A_Adelante.direction = Direction.OUTPUT
Motor_A_Atras.direction = Direction.OUTPUT
Motor_B_Adelante.direction = Direction.OUTPUT
Motor_B_Atras.direction = Direction.OUTPUT

# Definir pines PWM para Enable A y Enable B
Enable_A = pwmio.PWMOut(board.GP20, frequency=1000, duty_cycle=65535)  # Máxima velocidad
Enable_B = pwmio.PWMOut(board.GP21, frequency=1000, duty_cycle=65535)  # Máxima velocidad

def adelante():
    Motor_A_Adelante.value = True
    Motor_B_Adelante.value = True
    Motor_A_Atras.value = False
    Motor_B_Atras.value = False

def atras():
    Motor_A_Adelante.value = False
    Motor_B_Adelante.value = False
    Motor_A_Atras.value = True
    Motor_B_Atras.value = True

def detener():
    Motor_A_Adelante.value = False
    Motor_B_Adelante.value = False
    Motor_A_Atras.value = False
    Motor_B_Atras.value = False

def izquierda():
    Motor_A_Adelante.value = True
    Motor_B_Adelante.value = False
    Motor_A_Atras.value = False
    Motor_B_Atras.value = True

def derecha():
    Motor_A_Adelante.value = False
    Motor_B_Adelante.value = True
    Motor_A_Atras.value = True
    Motor_B_Atras.value = False

detener()

# Configurar conexión WiFi
wifi.radio.connect(ssid, password)
ip = wifi.radio.ipv4_address
print(f'Conectado con IP: {ip}')

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket()
server.bind((str(ip), 80))
server.listen(1)

def serve():
    while True:
        conn, addr = server.accept()
        buffer = bytearray(1024)
        conn.recv_into(buffer)  # Usar recv_into en CircuitPython
        request = str(buffer, 'utf-8')
        
        if '/adelante' in request:
            adelante()
        elif '/izquierda' in request:
            izquierda()
        elif '/detener' in request:
            detener()
        elif '/derecha' in request:
            derecha()
        elif '/atras' in request:
            atras()
        
        html = """
        <!DOCTYPE html>
        <html>
        <body>
        <form action="./adelante"><button>Adelante</button></form>
        <form action="./izquierda"><button>Izquierda</button></form>
        <form action="./detener"><button>Detener</button></form>
        <form action="./derecha"><button>Derecha</button></form>
        <form action="./atras"><button>Atras</button></form>
        </body>
        </html>
        """
        conn.send(html.encode())
        conn.close()

try:
    serve()
except KeyboardInterrupt:
    server.close()
    microcontroller.reset()
