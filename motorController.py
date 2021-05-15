#!/usr/bin/python3

import RPi.GPIO as GPIO
import time


# info: https://projects.raspberrypi.org/en/projects/robotPID/2

class Motor(object):
    def __init__(self, en, in_1, in_2):
        self._en = en
        self._in_1 = in_1
        self._in_2 = in_2
        GPIO.setup(self._en, GPIO.OUT)
        self._pwm = GPIO.PWM(self._en, 100)
        self._pwm.start(0)
        GPIO.setup(self._in_1, GPIO.OUT)
        GPIO.setup(self._in_2, GPIO.OUT)

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


GPIO.setmode(GPIO.BOARD)
m1 = Motor(18, 24, 22)
m2 = Motor(31, 26, 29)

try:
    m1.rotate(False, 100)
    m2.rotate(False, 100)
    for i in range(0, 100 + 1):
        if i % 10 == 0:
            print("PWM: {}".format(i))
        m1.rotate(False, i)
        m2.rotate(False, i)
        time.sleep(0.05)
    m1.rotate(True, 100)
    m2.rotate(True, 100)
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # quit
    m1.stop()
    m2.stop()
    GPIO.cleanup()
    print(" exit")
    exit()
