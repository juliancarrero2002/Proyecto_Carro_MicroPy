import time
import network
import socket
from machine import Pin, I2C, PWM, ADC
import ssd1306

# Configurar la pantalla OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configuración de los pines del motor
Motor_A_Adelante = Pin(18, Pin.OUT)
Motor_A_Atras = Pin(19, Pin.OUT)
Motor_B_Adelante = Pin(20, Pin.OUT)
Motor_B_Atras = Pin(21, Pin.OUT)

# Configuración de PWM para control de velocidad
PWM_A = PWM(Pin(14))  # PWM para el Motor A
PWM_B = PWM(Pin(15))  # PWM para el Motor B
PWM_A.freq(13)  # Frecuencia PWM para el Motor A
PWM_B.freq(13)  # Frecuencia PWM para el Motor B

# Función para establecer la velocidad de los motores
def set_speed(speed):
    duty = int(speed * 65535 / 100)  # Convertir porcentaje de velocidad a rango de PWM
    PWM_A.duty_u16(duty)
    PWM_B.duty_u16(duty)

# Función para conectar a la red WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Infinix2', 'juseca482020')
    
    while not wlan.isconnected():
        print("Conectando a la red WiFi...")
        time.sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'Conectado con IP: {ip}')
    return ip

# Configurar el socket UDP
def configurar_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, 12345))
    return s

# Función para controlar el movimiento del carro
def controlar_carro(x, y):
    velocidad = 100  # Ajusta la velocidad en porcentaje (0 a 100)
    
    if y > 2.5:  # Adelante
        Motor_A_Adelante.value(1)
        Motor_B_Adelante.value(1)
        Motor_A_Atras.value(0)
        Motor_B_Atras.value(0)
        set_speed(velocidad)
        
    elif y < 0.8:  # Atrás
        Motor_A_Adelante.value(0)
        Motor_B_Adelante.value(0)
        Motor_A_Atras.value(1)
        Motor_B_Atras.value(1)
        set_speed(velocidad)
        
    elif x > 2.5:  # Derecha
        Motor_A_Adelante.value(0)
        Motor_B_Adelante.value(1)
        Motor_A_Atras.value(1)
        Motor_B_Atras.value(0)
        set_speed(velocidad)
        
    elif x < 0.8:  # Izquierda
        Motor_A_Adelante.value(1)
        Motor_B_Adelante.value(0)
        Motor_A_Atras.value(0)
        Motor_B_Atras.value(1)
        set_speed(velocidad)
        
    else:  # Detener
        Motor_A_Adelante.value(0)
        Motor_B_Adelante.value(0)
        Motor_A_Atras.value(0)
        Motor_B_Atras.value(0)
        set_speed(0)  # Detener

# Función para recibir datos del joystick y mostrar en la pantalla OLED
def recibir_datos(socket, ip):
    while True:
        data, _ = socket.recvfrom(1024)
        x_value, y_value = map(float, data.decode().split(","))
        
        # Mostrar valores en el OLED
        display.fill(0)
        display.text(f'X: {x_value:.2f} V', 0, 0, 1)
        display.text(f'Y: {y_value:.2f} V', 0, 10, 1)
        display.text(f'IP: {ip}', 0, 20, 1)
        display.show()
        
        # Controlar el carro
        controlar_carro(x_value, y_value)
        time.sleep(0.1)

# Iniciar conexión WiFi y recepción de datos
ip = conectar_wifi()
socket = configurar_socket(ip)
recibir_datos(socket, ip)