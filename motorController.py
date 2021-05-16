#!/usr/bin/python3

import RPi.GPIO as GPIO
import Encoder
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

try:
    for i in range(0, 100 + 1):
        if i % 10 == 0:
            print("PWM: {}".format(i))
            print("Encoder pos: {}".format(m1.encoder.read()))
            print("Encoder pos: {}".format(m2.encoder.read()))
        m1.rotate(False, i)
        m2.rotate(False, i)
        time.sleep(0.05)

    for i in range(0, 100 + 1):
        if i % 10 == 0:
            print("PWM: {}".format(i))
            print("Encoder pos: {}".format(m1.encoder.read()))
            print("Encoder pos: {}".format(m2.encoder.read()))
        m1.rotate(True, i)
        m2.rotate(True, i)
        time.sleep(0.05)

    stop_all()

except KeyboardInterrupt:
    # quit
    stop_all()
