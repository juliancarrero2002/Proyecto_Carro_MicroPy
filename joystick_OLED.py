from machine import ADC, Pin, I2C
import ssd1306
import time

# Configurar el I2C para el display OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configurar el joystick
x_axis = ADC(Pin(26))  # VRX conectado a GP26
y_axis = ADC(Pin(27))  # VRY conectado a GP27
button = Pin(22, Pin.IN, Pin.PULL_UP)  # SW conectado a GP22

while True:
    # Leer los valores del joystick
    x_value = x_axis.read_u16() * 3.3 / 65535
    y_value = y_axis.read_u16() * 3.3 / 65535
    button_state = not button.value()

    # Limpiar la pantalla
    display.fill(0)

    # Mostrar los valores en el display
    display.text('X: {:.2f} V'.format(x_value), 0, 0, 1)
    display.text('Y: {:.2f} V'.format(y_value), 0, 10, 1)
    display.text('Button: {}'.format('Pressed' if button_state else 'Released'), 0, 20, 1)

    # Actualizar el display
    display.show()
  
    time.sleep(1)
