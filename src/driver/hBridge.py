"""
chip: TB6612FNG
or https://toshiba.semicon-storage.com/info/docget.jsp?did=10660&prodName=TB6612FNG
"""

import RPi.GPIO as GPIO
from enum import Enum, IntEnum


class TB6612FNG(IntEnum):
    # connected pins (BCM layout)
    # datasheet: 2. 5 & 6 and kicad pcb
    STBY = 23
    AIN1 = 25
    AIN2 = 24
    PWMA = 12
    BIN1 = 8
    BIN2 = 7
    PWMB = 13


class MotorDir(Enum):
    clockwise = True
    anticlockwise = False


class HBridge(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pin in TB6612FNG:
            GPIO.setup(pin, GPIO.OUT)

        self._IN1 = [TB6612FNG.AIN1, TB6612FNG.BIN1]
        self._IN2 = [TB6612FNG.AIN2, TB6612FNG.BIN2]
        self._PWM = [GPIO.PWM(TB6612FNG.PWMA, 1000), GPIO.PWM(TB6612FNG.PWMB, 1000)]
        self._PWM[0].start(0)
        self._PWM[1].start(0)
        self.set_standby(False)

    def drive(self, channel, direction: MotorDir, speed):
        """
        drives both motors

        :param channel: 0 (lower) or 1 (upper)
        :param direction: clockwise or counter clockwise
        :param speed: 0 - 100
        """
        a = GPIO.HIGH if direction == MotorDir.clockwise else GPIO.LOW
        b = GPIO.HIGH if direction != MotorDir.clockwise else GPIO.LOW

        GPIO.output(self._IN1[channel], a)
        GPIO.output(self._IN2[channel], b)

        self._PWM[channel].ChangeDutyCycle(speed)

    def set_standby(self, state):
        """
        sets chip to standby, both motors wont spin
        :param state: true / false
        """
        state = GPIO.LOW if state else GPIO.HIGH
        GPIO.output(TB6612FNG.STBY, state)

    def stop_channel(self, channel):
        """
        sets channel into stop mode (high impedance)
        :param channel: 0 (lower) or 1 (upper)
        """
        GPIO.output(self._IN1[channel], GPIO.LOW)
        GPIO.output(self._IN2[channel], GPIO.LOW)
        self._PWM[channel].ChangeDutyCycle(0)
