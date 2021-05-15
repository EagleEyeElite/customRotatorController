#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

enB = 33
in4 = 31
in3 = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(enB, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.output(enB, GPIO.HIGH)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

pwm = GPIO.PWM(enB, 100)
pwm.start(0)


def rotate(direction):
    if direction:
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
    else:
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)


try:
    pwm.ChangeDutyCycle(100)
    rotate(False)
    for i in range(0, 100 + 1):
        if i % 10 == 0:
            print("PWM: {}".format(i))
        pwm.ChangeDutyCycle(i)
        time.sleep(0.05)
    rotate(True)
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # quit
    GPIO.cleanup()
    print(" exit")
    exit()
