import RPi.GPIO as GPIO

LED_PIN = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def ON():
    GPIO.output(LED_PIN, 1)

def OFF():
    GPIO.output(LED_PIN, 0)

if __name__ == '__main__':
    from time import sleep
    while True:
        ON()
        sleep(1)
        OFF()
        sleep(1)
