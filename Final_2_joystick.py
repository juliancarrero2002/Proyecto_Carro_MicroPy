import time
import network
import socket
from machine import Pin, ADC

# Configurar el joystick
x_axis = ADC(Pin(26))  # VRX conectado a GP26
y_axis = ADC(Pin(27))  # VRY conectado a GP27
button = Pin(22, Pin.IN, Pin.PULL_UP)  # SW conectado a GP22

# Conexión WiFi
ssid = 'Infinix2'
password = 'juseca482020'

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        print("Conectando a la red WiFi...")
        time.sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'Conectado con IP: {ip}')
    return wlan

def enviar_datos(ip_receptor):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        # Leer los valores del joystick
        x_value = x_axis.read_u16() * 3.3 / 65535
        y_value = y_axis.read_u16() * 3.3 / 65535
        
        # Enviar datos al receptor
        mensaje = f"{x_value},{y_value}"
        s.sendto(mensaje.encode(), (ip_receptor, 12345))
        
        time.sleep(0.1)

wlan = conectar_wifi()
# Reemplaza '192.168.0.XX' con la IP de la Raspberry Pi Pico W 2
enviar_datos('192.168.218.151')