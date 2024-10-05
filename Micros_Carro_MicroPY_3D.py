import network
import socket
from time import sleep
import machine
from machine import Pin

ssid = 'Infinix2'
password = 'juseca482020'

Motor_A_Adelante = Pin(18, Pin.OUT)
Motor_A_Atras = Pin(19, Pin.OUT)
Motor_B_Adelante = Pin(20, Pin.OUT)
Motor_B_Atras = Pin(21, Pin.OUT)

def adelante():
    Motor_A_Adelante.value(1)
    Motor_B_Adelante.value(1)
    Motor_A_Atras.value(0)
    Motor_B_Atras.value(0)
    
def atras():
    Motor_A_Adelante.value(0)
    Motor_B_Adelante.value(0)
    Motor_A_Atras.value(1)
    Motor_B_Atras.value(1)

def detener():
    Motor_A_Adelante.value(0)
    Motor_B_Adelante.value(0)
    Motor_A_Atras.value(0)
    Motor_B_Atras.value(0)

def izquierda():
    Motor_A_Adelante.value(1)
    Motor_B_Adelante.value(0)
    Motor_A_Atras.value(0)
    Motor_B_Atras.value(1)

def derecha():
    Motor_A_Adelante.value(0)
    Motor_B_Adelante.value(1)
    Motor_A_Atras.value(1)
    Motor_B_Atras.value(0)


detener()
    
def conectar():
    red = network.WLAN(network.STA_IF)
    red.active(True)
    red.connect(ssid, password)
    while red.isconnected() == False:
        print('Conectando ...')
        sleep(1)
    ip = red.ifconfig()[0]
    print(f'Conectado con IP: {ip}')
    return ip
    
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def pagina_web():
    html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                <style>
                    body { margin: 0; overflow: hidden; }
                    #container { position: absolute; width: 100%; height: 100%; }
                    #controls { position: absolute; top: 10px; left: 50%; transform: translateX(-50%); z-index: 1; }
                    #controls button { background-color: #04AA6D; border-radius: 15px; height: 40px; width: 80px; border: none; color: white; margin: 5px; cursor: pointer; }
                    #controls button#detener { background-color: #FF0000; border-radius: 50%; }
                </style>
            </head>
            <body>
                <div id="container"></div>
                <div id="controls">
                    <form action="./adelante"><button type="submit">Adelante</button></form>
                    <form action="./izquierda"><button type="submit">Izquierda</button></form>
                    <form action="./detener"><button type="submit" id="detener">Detener</button></form>
                    <form action="./derecha"><button type="submit">Derecha</button></form>
                    <form action="./atras"><button type="submit">Atrás</button></form>
                </div>
                <script>
                    // Inicializar escena
                    const scene = new THREE.Scene();
                    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                    const renderer = new THREE.WebGLRenderer();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    document.getElementById('container').appendChild(renderer.domElement);

                    // Crear un cubo
                    const geometry = new THREE.BoxGeometry();
                    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
                    const cube = new THREE.Mesh(geometry, material);
                    scene.add(cube);

                    camera.position.z = 5;

                    // Animación
                    function animate() {
                        requestAnimationFrame(animate);
                        cube.rotation.x += 0.01;
                        cube.rotation.y += 0.01;
                        renderer.render(scene, camera);
                    }
                    animate();

                    // Ajustar el tamaño de la ventana
                    window.addEventListener('resize', () => {
                        const width = window.innerWidth;
                        const height = window.innerHeight;
                        renderer.setSize(width, height);
                        camera.aspect = width / height;
                        camera.updateProjectionMatrix();
                    });
                </script>
            </body>
            </html>
            """
    return html

def serve(connection):
    while True:
        cliente = connection.accept()[0]
        peticion = cliente.recv(1024)
        peticion = str(peticion)
        try:
            peticion = peticion.split()[1]
        except IndexError:
            pass
        if peticion == '/adelante?':
            adelante()
        elif peticion =='/izquierda?':
            izquierda()
        elif peticion =='/detener?':
            detener()
        elif peticion =='/derecha?':
            derecha()
        elif peticion =='/atras?':
            atras()
        html = pagina_web()
        cliente.send(html)
        cliente.close()

try:
    ip = conectar()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()