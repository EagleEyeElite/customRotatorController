#!/usr/bin/python3

import RPi.GPIO as GPIO
from motor import Motor
from rotator import Rotator, dirEe
import time
import sys


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    rotator = Rotator(Motor(24, 8, 25, 17, 27), Motor(6, 7, 5, 22, 23))
    try:
        for line in sys.stdin:
            if 'w' == line.rstrip():
                rotator.direction(dirEe.up, 2000)
            if 'a' == line.rstrip():
                rotator.direction(dirEe.down, 2000)
            if 's' == line.rstrip():
                rotator.direction(dirEe.clockwise, 2000)
            if 'd' == line.rstrip():
                rotator.direction(dirEe.anticlockwise, 2000)

    except KeyboardInterrupt:
        pass

    # quit
    rotator.stop()
    time.sleep(0.5)     # wait for motor encoder to stop
    GPIO.cleanup()
    print(" exit")
    time.sleep(0.05)    # wait for stdout
    exit()
