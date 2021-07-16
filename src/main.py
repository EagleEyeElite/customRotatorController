#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from i2cHandler import I2cHandler
from driver.hBridge import HBridge, MotorDir
from shaft import Shaft
from driver.encoder import set_up_encoder
from driver.switch import Switch

# TODO implement Shaft Controller -> good name: Actuator?, use singleton classes or modules?

if __name__ == "__main__":
    """
    Software entry point
    """
    GPIO.setmode(GPIO.BCM)
    ens = set_up_encoder()
    h = HBridge()
    i2c = I2cHandler()
    sw = Switch()

    try:
        a0 = Shaft(0, ens[0], h, i2c)
        a1 = Shaft(1, ens[1], h, i2c)

        old_time = time.time()
        direction = MotorDir.clockwise
        a0.drive(direction, 50)
        a1.drive(direction, 50)

        while True:
            if time.time() - old_time >= 15:
                old_time = time.time()
                a0.drive(MotorDir.clockwise, 0)
                a1.drive(MotorDir.clockwise, 0)
                time.sleep(2)
                direction = MotorDir.clockwise if direction == MotorDir.anticlockwise else MotorDir.anticlockwise
                a0.drive(MotorDir.anticlockwise, 50)
                a1.drive(MotorDir.anticlockwise, 50)

            print(str(a0.get_encoder_pos()) + "\t" +
                  str(a0.get_magnetic_encoder_angle()) + "\t" +
                  str(a1.get_encoder_pos()) + "\t" +
                  str(a1.get_magnetic_encoder_angle()))
            time.sleep(0.2)

    except KeyboardInterrupt:
        pass

    # quit
    h.set_standby(True)
    time.sleep(0.5)  # wait for motor encoder to stop
    GPIO.cleanup()
    print(" exit")
    time.sleep(0.05)  # wait for stdout
    exit()
