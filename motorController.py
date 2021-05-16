#!/usr/bin/python3

import RPi.GPIO as GPIO
import Encoder
from simple_pid import PID
import time


# info: https://projects.raspberrypi.org/en/projects/robotPID/2

class Motor(object):
    def __init__(self, en, in_1, in_2, enc_1, enc_2):
        GPIO.setmode(GPIO.BCM)
        self._en = en
        self._in_1 = in_1
        self._in_2 = in_2
        GPIO.setup(self._en, GPIO.OUT)
        self._pwm = GPIO.PWM(self._en, 100)
        self._pwm.start(0)
        GPIO.setup(self._in_1, GPIO.OUT)
        GPIO.setup(self._in_2, GPIO.OUT)
        self.encoder = Encoder.Encoder(enc_1, enc_2)

    def rotate(self, direction, speed):
        if direction:
            GPIO.output(self._in_1, GPIO.HIGH)
            GPIO.output(self._in_2, GPIO.LOW)
        else:
            GPIO.output(self._in_1, GPIO.LOW)
            GPIO.output(self._in_2, GPIO.HIGH)
        self._pwm.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self._in_1, GPIO.HIGH)
        GPIO.output(self._in_2, GPIO.HIGH)
        self._pwm.ChangeDutyCycle(0)


def stop_all():
    m1.stop()
    m2.stop()
    time.sleep(0.5)
    GPIO.cleanup()
    print(" exit")

    time.sleep(0.05)
    exit()


GPIO.setmode(GPIO.BCM)
m1 = Motor(24, 8, 25, 17, 27)
m2 = Motor(6, 7, 5, 22, 23)

pid1 = PID(4, 3, 0, setpoint=180)
pid1.output_limits = (0, 100)
pid2 = PID(4, 3, 0, setpoint=180)
pid2.output_limits = (0, 100)

try:
    while True:
        control1 = pid1(m1.encoder.read())
        oldPos1 = m1.encoder.pos
        m1.encoder.pos = 0
        m1.rotate(True, control1)

        control2 = pid2(m2.encoder.read())
        oldPos2 = m2.encoder.pos
        m2.encoder.pos = 0
        m2.rotate(True, control2)

        print("PWM1: {}".format(control1))
        print("PWM2: {}".format(control2))
        print("Encoder pos1: {}".format(oldPos1))
        print("Encoder pos2: {}".format(oldPos2))

        time.sleep(0.05)

except KeyboardInterrupt:
    # quit
    stop_all()
