#!/usr/bin/python3

from enum import Enum
import threading
import time


class dirEe(Enum):
    up = 1
    down = 2
    clockwise = 3
    anticlockwise = 4


class Rotator(object):
    def __init__(self, m1, m2):
        self._m1 = m1
        self._m2 = m2
        self.stopSpeedControl = False
        self.speedControl = threading.Thread(target=self.control_motors_speed)
        self.speedControl.start()

    # timing: controlled by thread
    def control_motors_speed(self):
        ticker = threading.Event()
        while not ticker.wait(0.01):
            if self.stopSpeedControl:
                break
            self._m1.maintain_speed()
            self._m2.maintain_speed()

    def direction(self, dir_e, speed=500, time_s=4):
        if dir_e == dirEe.up:
            self._m1.rotate(True, speed)
            self._m2.rotate(True, speed)
            print("turn up")
        elif dir_e == dirEe.down:
            self._m1.rotate(False, speed)
            self._m2.rotate(False, speed)
            print("turn down")
        elif dir_e == dirEe.clockwise:
            self._m1.rotate(False, speed)
            self._m2.rotate(True, speed)
            print("turn clockwise")
        elif dir_e == dirEe.anticlockwise:
            self._m1.rotate(True, speed)
            self._m2.rotate(False, speed)
            print("turn anticlockwise")

        time.sleep(time_s)
        self._m1.rotate(False, 0)
        self._m2.rotate(True, 0)

    def stop(self):
        self._m1.stop()
        self._m2.stop()
        self.stopSpeedControl = True
        self.speedControl.join()
