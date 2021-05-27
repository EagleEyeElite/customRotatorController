#!/usr/bin/python3

import RPi.GPIO as GPIO
from motor import Motor
from rotator import Rotator, RotatorDir
import time
import sys


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    rotator = Rotator(Motor(24, 8, 25, 17, 27), Motor(6, 7, 5, 22, 23))
    try:

        speed = 500     # 2000 if motors are disconnected
        rotator.direction(RotatorDir.up, speed, 6)
        rotator.direction(RotatorDir.down, speed, 4)
        rotator.direction(RotatorDir.clockwise, speed, 6)
        rotator.direction(RotatorDir.down, speed, 2)
        rotator.direction(RotatorDir.anticlockwise, speed / 2, 12)

        for line in sys.stdin:
            if 'w' == line.rstrip():
                rotator.direction(RotatorDir.up, speed)
            if 's' == line.rstrip():
                rotator.direction(RotatorDir.down, speed)
            if 'd' == line.rstrip():
                rotator.direction(RotatorDir.clockwise, speed)
            if 'a' == line.rstrip():
                rotator.direction(RotatorDir.anticlockwise, speed)

    except KeyboardInterrupt:
        pass

    # quit
    rotator.stop()
    time.sleep(0.5)     # wait for motor encoder to stop
    GPIO.cleanup()
    print(" exit")
    time.sleep(0.05)    # wait for stdout
    exit()
