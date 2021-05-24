#!/usr/bin/python3

import RPi.GPIO as GPIO
from simple_pid import PID
import Encoder
import time


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

        self.pid = PID(0.1, 0, 0)
        self.pid.output_limits = (0, 100)
        self.lastTime = time.time()
        self.lastEncoderTicks = abs(self.encoder.read())
        self.startFix = 0

    def rotate(self, direction, speed):
        if direction:
            GPIO.output(self._in_1, GPIO.HIGH)
            GPIO.output(self._in_2, GPIO.LOW)
        else:
            GPIO.output(self._in_1, GPIO.LOW)
            GPIO.output(self._in_2, GPIO.HIGH)
        self.pid.setpoint = speed
        self.lastTime = time.time()
        self.lastEncoderTicks = abs(self.encoder.read())
        self.startFix = 0
        self.encoder.pos = 0

    # needs to be called regular (~every 0.01s)
    def maintain_speed(self):
        current_time = time.time()
        current_ticks = abs(self.encoder.read())
        self.startFix += 1
        if current_ticks == 0 and self.startFix > 10:
            return
        used_time = current_time - self.lastTime
        used_ticks = current_ticks - self.lastEncoderTicks
        speed = used_ticks / used_time

        pwm = self.pid(speed)
        self._pwm.ChangeDutyCycle(pwm)

        self.lastTime = current_time
        self.lastEncoderTicks = current_ticks

        # print("time: {}, ticks: {}, speed: {}, pwm: {}".format(used_time, currentTicks, speed, pwm))

    def stop(self):
        GPIO.output(self._in_1, GPIO.HIGH)
        GPIO.output(self._in_2, GPIO.HIGH)
        self._pwm.ChangeDutyCycle(0)
