"""
driver module to monitor switches,
"""

import RPi.GPIO as GPIO
from enum import IntEnum


class SwitchPins(IntEnum):
    switch0 = 17
    switch1 = 27
    switch2 = 22


class Switch(object):
    """
    initializes Pin usage and interrupt on button press
    """
    def __init__(self):
        self._sw = [SwitchPins.switch2, SwitchPins.switch0, SwitchPins.switch1]
        for pin in SwitchPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self._sw[0], GPIO.FALLING, callback=lambda x: self.button_callback(0), bouncetime=500)
        GPIO.add_event_detect(self._sw[1], GPIO.FALLING, callback=lambda x: self.button_callback(1), bouncetime=500)
        GPIO.add_event_detect(self._sw[2], GPIO.FALLING, callback=lambda x: self.button_callback(2), bouncetime=500)

    def button_callback(self, channel):
        """
        handles button press
        :param channel: button id
        :raises Exception on press
        """
        raise Exception("switch pressed:", channel)
