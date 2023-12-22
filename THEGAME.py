import machine
import utime
from machine import I2C, Pin
import ssd1306

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig = machine.Pin(trig_pin, machine.Pin.OUT)
        self.echo = machine.Pin(echo_pin, machine.Pin.IN)

    def get_distance(self):
        self.trig.value(1)
        utime.sleep_us(10)
        self.trig.value(0)

        while self.echo.value() == 0:
            pulse_start = utime.ticks_us()

        while self.echo.value() == 1:
            pulse_end = utime.ticks_us()

        pulse_duration = utime.ticks_diff(pulse_end, pulse_start)
        distance = pulse_duration / 58.0

        return distance

class MicrowaveDoppler:
    _start_time = 0

    @staticmethod
    def begin():
        Pin(16, Pin.IN)  # Set up pin for input

    @staticmethod
    def get_period():
        while True:
            if Pin(16).value() == 1:  # Wait for rising edge
                start_time = utime.ticks_us()
                while Pin(16).value() == 1:  # Wait for falling edge
                    pass
                end_time = utime.ticks_us()
                return utime.ticks_diff(end_time, start_time)

def setup():
    print("Setup Ultrasonic Sensors and Microwave Doppler Radar")
    MicrowaveDoppler.begin()

def loop():
    try:
        distance1 = ultrasonic_sensor1.get_distance()
        distance2 = ultrasonic_sensor2.get_distance()

        # LED and Buzzer control based on distance for Sensor 1
        if distance1 > 20:
            green_led.value(1)
            blue_led.value(0)
            red_led.value(0)
            buzzer.value(0)
        elif 10 <= distance1 <= 20:
            green_led.value(0)
            blue_led.value(1)
            red_led.value(0)
            buzzer.value(0)
        else:
            green_led.value(0)
            blue_led.value(0)
            red_led.value(1)
            buzzer.value(1)

        oled.fill(0)
        oled.text("Blind Spot",0, 0)
        oled.text("D 1: {:.2f} cm".format(distance1), 0, 16)

        # LED and Buzzer control based on distance for Sensor 2
        if distance2 > 20:
            green_led.value(1)
            blue_led.value(0)
            red_led.value(0)
            buzzer.value(0)
        elif 10 <= distance2 <= 20:
            green_led.value(0)
            blue_led.value(1)
            red_led.value(0)
            buzzer.value(0)
        else:
            green_led.value(0)
            blue_led.value(0)
            red_led.value(1)
            buzzer.value(1)

        oled.text("D 2: {:.2f} cm".format(distance2), 0, 24)

        period = MicrowaveDoppler.get_period()
        if period:
            frequency = 1 / (period * 1e-6)
            speed_kmph = frequency * (3.6 / 31.36)
            oled.text("Speed: {:.2f} km/h".format(speed_kmph), 0, 32)

        oled.show()
        utime.sleep(1)

    except KeyboardInterrupt:
        print("\nScript terminated by user (Ctrl+C)")
        raise SystemExit

# Define the GPIO pins for the ultrasonic sensors
trigPin1 = 6
echoPin1 = 7
trigPin2 = 8
echoPin2 = 9

ultrasonic_sensor1 = UltrasonicSensor(trigPin1, echoPin1)
ultrasonic_sensor2 = UltrasonicSensor(trigPin2, echoPin2)

# Define the LED and buzzer pins
green_led_pin = 12
blue_led_pin = 14
red_led_pin = 15
buzzer_pin = 17

# Initialize the LED and buzzer pins
green_led = machine.Pin(green_led_pin, machine.Pin.OUT)
blue_led = machine.Pin(blue_led_pin, machine.Pin.OUT)
red_led = machine.Pin(red_led_pin, machine.Pin.OUT)
buzzer = machine.Pin(buzzer_pin, machine.Pin.OUT)

# Initialize the I2C interface and OLED display
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Run setup once
setup()

# Main loop
while True:
    # Run the loop continuously
    loop()
