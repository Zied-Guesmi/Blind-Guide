import RPi.GPIO as GPIO
import time
import os
from image_to_speech import ImageToSpeech
from obstacle_detector import ObstacleDetector

class Main(object):
    """docstring for Main."""
    def __init__(self, arg):
        super(Main, self).__init__()
        self.arg = arg

    def setup(arg):
        logging.basicConfig(filename='/tmp/blind-assistant.log', level=logging.INFO)
        logging.info('Started')
        ObstacleDetector.do_something()
        logging.info('Finished')


language = "EN"

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_MODE_BUTTON = 16
GPIO_CAPTURE_BUTTON = 25

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

GPIO.setup(GPIO_MODE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_CAPTURE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Allow module to settle
time.sleep(0.1)

GPIO.add_event_detect(GPIO_MODE_BUTTON, GPIO.BOTH)
GPIO.add_event_detect(GPIO_CAPTURE_BUTTON, GPIO.FALLING)

os.system("amixer set PCM -- 100%")

while True:
    print("====> Obstacle detection mode")
    obstacle_detection_mode(GPIO_TRIGGER, GPIO_ECHO, language)

    if GPIO.event_detected(GPIO_MODE_BUTTON) and GPIO.input(GPIO_MODE_BUTTON) == False:
        print("====> Camera mode")
        while True:
            if GPIO.event_detected(GPIO_CAPTURE_BUTTON):
                camera_mode(camera)
            elif GPIO.event_detected(GPIO_MODE_BUTTON) and GPIO.input(GPIO_MODE_BUTTON) == True:
                break
    time.sleep(0.1)