#!/usr/bin/python3
import threading

import RPi.GPIO as GPIO
import time
import interface
from controller.controller import Controller
import sys

# TODO implement Shaft Controller -> good name: Actuator?, use singleton classes or modules?


if __name__ == "__main__":
    """
    Software entry point
    """

    rC = interface.Configuration()
    controller = Controller(rC)
    rotctl = interface.RotCtl(rC)

    t0 = threading.Thread(target=rotctl.run)
    t1 = threading.Thread(target=controller.run)

    try:
        t0.start()
        t1.start()
        while True:
            # controller.print_debug()
            time.sleep(1)
            pass

    except KeyboardInterrupt:
        pass

    # quit
    # h.set_standby(True) # TODO move into Controller
    rotctl.stop()
    controller.stop()
    t1.join(timeout=0.2)
    t0.join(timeout=0.2)
    time.sleep(0.5)  # wait for motor encoder to stop
    GPIO.cleanup()
    print(" exit")
    time.sleep(0.05)  # wait for stdout
    sys.exit(0)
