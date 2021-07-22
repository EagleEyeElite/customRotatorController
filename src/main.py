#!/usr/bin/python3
import threading

import RPi.GPIO as GPIO
import time
from i2cHandler import I2cHandler
from driver.hBridge import HBridge, MotorDir
from shaft import Shaft
from driver.encoder import set_up_encoder
from driver.switch import Switch
from rotctl import RotCtl
from configuration import Configuration
from Controller import Controller

# TODO implement Shaft Controller -> good name: Actuator?, use singleton classes or modules?


if __name__ == "__main__":
    """
    Software entry point
    """

    rC = Configuration()
    controller = Controller(rC)
    rotctl = RotCtl(rC)

    t0 = threading.Thread(target=rotctl.run)
    t1 = threading.Thread(target=controller.run)

    try:
        t0.start()
        t1.start()
        while True:
            rC.print_debug()
            time.sleep(0.1)
            pass

    except KeyboardInterrupt:
        pass

    # quit
    # h.set_standby(True) # TODO move into Controller
    time.sleep(0.5)  # wait for motor encoder to stop
    GPIO.cleanup()
    print(" exit")
    time.sleep(0.05)  # wait for stdout
    exit()
