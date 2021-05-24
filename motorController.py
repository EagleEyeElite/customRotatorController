#!/usr/bin/python3

import RPi.GPIO as GPIO
from simple_pid import PID
import Encoder
from enum import Enum
import threading
import time
import sys


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


# timing:
def control_motors_speed(stop):
    ticker = threading.Event()
    while not ticker.wait(0.01):
        if stop():
            break
        m1.maintain_speed()
        m2.maintain_speed()


class dirEe(Enum):
    up = 1
    down = 2
    clockwise = 3
    anticlockwise = 4


def direction(dir_e, speed=500):
    if dir_e == dirEe.up:
        m1.rotate(True, speed)
        m2.rotate(True, speed)
        print("turn up")
    elif dir_e == dirEe.down:
        m1.rotate(False, speed)
        m2.rotate(False, speed)
        print("turn down")
    elif dir_e == dirEe.clockwise:
        m1.rotate(False, speed)
        m2.rotate(True, speed)
        print("turn clockwise")
    elif dir_e == dirEe.anticlockwise:
        m1.rotate(True, speed)
        m2.rotate(False, speed)
        print("turn anticlockwise")

    time.sleep(4)
    m1.rotate(False, 0)
    m2.rotate(True, 0)


GPIO.setmode(GPIO.BCM)
m1 = Motor(24, 8, 25, 17, 27)
m2 = Motor(6, 7, 5, 22, 23)

stop_threads = False
th = threading.Thread(target=control_motors_speed, args=(lambda: stop_threads,))
th.start()

try:
    while True:
        for line in sys.stdin:
            if 'w' == line.rstrip():
                direction(dirEe.up, 2000)
            if 'a' == line.rstrip():
                direction(dirEe.down, 2000)
            if 's' == line.rstrip():
                direction(dirEe.clockwise, 2000)
            if 'd' == line.rstrip():
                direction(dirEe.anticlockwise, 2000)

except KeyboardInterrupt:
    pass

# quit
m1.stop()
m2.stop()
stop_threads = True
th.join()
time.sleep(0.5)
GPIO.cleanup()
print(" exit")

time.sleep(0.05)
exit()
