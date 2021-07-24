from .shaft import Shaft
import RPi.GPIO as GPIO


class Rotator(object):
    def __init__(self, shaft: [Shaft, Shaft]):
        GPIO.setmode(GPIO.BCM)
        self.shaft = shaft


