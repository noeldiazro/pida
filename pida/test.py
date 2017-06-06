from gpio import GPIO, LED, Direction, Status, Edge
from time import time
import RPi.GPIO

def test_streamed(n_samples):
    with GPIO(18) as led:
        led.direction = Direction.OUTPUT
        with led.get_stream_writer() as writer:
            start = time()
            for _ in range(n_samples):
                writer.write('1')
                writer.write('0')
            end = time()
    return (end - start) / n_samples

def test_not_streamed(n_samples):
    with GPIO(18) as led:
        led.direction = Direction.OUTPUT
        start = time()
        for _ in range(n_samples):
            led.status = Status.HIGH
            led.status = Status.LOW
        end = time()
    return (end - start) / n_samples

def test_rpi_gpio(n_samples):
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setup(18, RPi.GPIO.OUT)
    start = time()
    for _ in range(n_samples):
        RPi.GPIO.output(18, RPi.GPIO.HIGH)
        RPi.GPIO.output(18, RPi.GPIO.LOW)
    end = time()
    return (end - start) / n_samples

def test_button():
    with GPIO(25) as button:
        button.direction = Direction.INPUT
        button.edge = Edge.RISING

        counter = 0
        while True:
            button.wait_for_edge()
            counter += 1
            print(counter)

def test_button_led():
    with LED(18) as led:
        with GPIO(25) as button:
            button.direction = Direction.INPUT
            button.edge = Edge.RISING

            while True:
                button.wait_for_edge()
                led.toggle()

def test_button_led2():
    with LED(18) as led:
        with GPIO(25) as button:
            button.direction = Direction.INPUT
            button.edge = Edge.BOTH

            while True:
                button.wait_for_edge()
                if button.status == Status.HIGH:
                    led.switch_on()
                else:
                    led.switch_off()

