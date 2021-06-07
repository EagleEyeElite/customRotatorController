#!/usr/bin/python3

from enum import Enum
import threading
import time
from motor import MotorDir


class RotatorDir(Enum):
    up = 1
    down = 2
    clockwise = 3
    anticlockwise = 4


class Rotator(object):
    def __init__(self, m0, m1):
        self._m0 = m0
        self._m1 = m1
        self.stopSpeedControl = False
        self.speedControl = threading.Thread(target=self.control_motors_speed)
        self.speedControl.start()

    # timing: controlled by thread
    def control_motors_speed(self):
        ticker = threading.Event()
        while not ticker.wait(0.01):
            if self.stopSpeedControl:
                break
            self._m0.maintain_speed(0)
            self._m1.maintain_speed(1)

    def direction(self, dir_e, speed=500, time_s=4):
        if dir_e == RotatorDir.up:
            self._m0.rotate(MotorDir.clockwise, speed)
            self._m1.rotate(MotorDir.clockwise, speed)
            print("turn up")
        elif dir_e == RotatorDir.down:
            self._m0.rotate(MotorDir.anticlockwise, speed)
            self._m1.rotate(MotorDir.anticlockwise, speed)
            print("turn down")
        elif dir_e == RotatorDir.clockwise:
            self._m0.rotate(MotorDir.anticlockwise, speed)
            self._m1.rotate(MotorDir.clockwise, speed)
            print("turn clockwise")
        elif dir_e == RotatorDir.anticlockwise:
            self._m0.rotate(MotorDir.clockwise, speed)
            self._m1.rotate(MotorDir.anticlockwise, speed)
            print("turn anticlockwise")

        time.sleep(time_s)
        self._m0.rotate(False, 0)
        self._m1.rotate(True, 0)

    def stop(self):
        self._m0.stop()
        self._m1.stop()
        self.stopSpeedControl = True
        self.speedControl.join()
