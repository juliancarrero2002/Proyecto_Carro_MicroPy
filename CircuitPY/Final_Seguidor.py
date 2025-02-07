import time
import board
import digitalio
import pwmio
from digitalio import DigitalInOut, Direction
import socketpool
import wifi
import os  # Asumiendo que hay un sistema de archivos disponible

# Importar el método API desde un archivo separado
from api import api

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

# Funciones de movimiento del robot
def move_forward():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = True
    Motor_A_Atras.value = False
    Motor_B_Adelante.value = True
    Motor_B_Atras.value = False

def move_backward():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = False
    Motor_A_Atras.value = True
    Motor_B_Adelante.value = False
    Motor_B_Atras.value = True

def turn_right():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = True
    Motor_A_Atras.value = False
    Motor_B_Adelante.value = False
    Motor_B_Atras.value = False
    time.sleep(0.5)
    stop()

def turn_left():
    Motor_A_Adelante.direction = Direction.OUTPUT
    Motor_A_Atras.direction = Direction.OUTPUT
    Motor_B_Adelante.direction = Direction.OUTPUT
    Motor_B_Atras.direction = Direction.OUTPUT
    
    Motor_A_Adelante.value = False
    Motor_A_Atras.value = False
    Motor_B_Adelante.value = True
    Motor_B_Atras.value = False
    time.sleep(0.5)
    stop()

def stop():
    Motor_A_Adelante.value = False
    Motor_A_Atras.value = False
    Motor_B_Adelante.value = False
    Motor_B_Atras.value = False

# Funciones del servidor
def start_server(ap=True):
    if ap:
        wifi.radio.start_ap("RPi-Pico", "12345678")
        print("wifi.radio ap:", wifi.radio.ipv4_address_ap)
    else:
        wifi.radio.connect("Infinix3", "juseca7216")
        print("wifi.radio:", wifi.radio.ipv4_address)
        
    pool = socketpool.SocketPool(wifi.radio)
    
    s = pool.socket()
    s.bind(('', 80))
    s.listen(5)
    return s

def get_content_type(filename):
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        return 'image/jpeg'
    elif filename.endswith('.gif'):
        return 'image/gif'
    else:
        return 'application/octet-stream'

def file_exists(filename):
    directory = '.'  # Directorio donde se almacenan los archivos
    files = os.listdir(directory)
    return filename.lstrip('/') in files

def handle_request(client):
    buffer = bytearray(1024)
    bytes_received, address = client.recvfrom_into(buffer)
    request = buffer[:bytes_received]
    request_str = request.decode('utf-8')

    # Extraer el archivo solicitado
    try:
        request_file = request_str.split(' ')[1]
        print('request_file', request_file)
        if request_file == '/':
            request_file = '/index.html'  # Por defecto a index.html
    except IndexError:
        client.send('HTTP/1.1 400 Bad Request\r\n')
        client.close()
        return

    # Comprobar si la solicitud es para el endpoint de la API
    if request_file.startswith('/api'):
        response = api(request_str)
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: application/octet-stream\r\n")
        client.send("Connection: close\r\n\r\n")
        client.send(response)
        client.close()
        return

    # Comprobar si el archivo existe
    if file_exists(request_file):
        print('file_exists')
        content_type = get_content_type(request_file)

        # Enviar encabezados
        client.send('HTTP/1.1 200 OK\r\n')
        client.send(f"Content-Type: {content_type}\r\n")
        client.send("Connection: close\r\n\r\n")

        # Leer y enviar el archivo
        with open(request_file, 'rb') as f:
            client.send(f.read())
    else:
        client.send('HTTP/1.1 404 Not Found\r\n')
    
    client.close()

# Iniciar el servidor y el bucle de control del robot
server = start_server()

while True:
    right_val = right_ir.value
    left_val = left_ir.value

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

    # Aceptar conexiones de clientes
    client, addr = server.accept()
    print("Cliente conectado desde:", addr)
    handle_request(client)