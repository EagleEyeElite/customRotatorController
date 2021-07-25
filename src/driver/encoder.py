"""
includes functionality to monitor the motors encoders
"""

import RPi.GPIO as GPIO
import Encoder
from enum import IntEnum


class EncoderPins(IntEnum):
    encoder0_m0 = 5
    encoder1_m0 = 6
    encoder0_m1 = 26
    encoder1_m1 = 16


def set_up_encoder() -> Encoder:
    """
    set up encoder GPIO
    :return: ready to use encoder object list
    """
    for pin in EncoderPins:
        GPIO.setup(pin, GPIO.OUT)
    encoder = [Encoder.Encoder(EncoderPins.encoder1_m1, EncoderPins.encoder0_m1),
               Encoder.Encoder(EncoderPins.encoder1_m0, EncoderPins.encoder0_m0)]
    return encoder
