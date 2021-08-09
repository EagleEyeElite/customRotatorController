import time
import RPi.GPIO as GPIO
from logzero import logger

from .I2cHandler import I2cHandler
from .Shaft import Shaft
import driver
import interface


class SatelliteReceiver(object):
    """
    This object reflect the satellite receiver.
    It provides functions to move the rotator and readout all sensors.
    For better abstraction the receiver is made up from 2 shafts.
    The differential is driven by both shafts.
    """
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        ens = driver.encoder.set_up_encoder()
        self.h = driver.hBridge.HBridge()
        i2c = I2cHandler()
        offset = [i2c.get_magnetic_encoder(0).get_raw_angle(),
                  i2c.get_magnetic_encoder(1).get_raw_angle()]
        self.shaft = [Shaft(0, ens[0], self.h, i2c, offset[0]),
                      Shaft(1, ens[1], self.h, i2c, offset[1])]
        self.sw = driver.switch.Switch()

    def stop(self):
        self.shaft[0].stop()
        self.shaft[1].stop()

    def exit(self):
        self.h.set_standby(True)
        time.sleep(0.5)  # wait for motor encoder to stop
        GPIO.cleanup()

    def get_rec_pos(self) -> [int, int]:
        """
        :return: [azimuth, elevation]
        """
        shaft_angle = [self.shaft[0].get_motor_angle(), self.shaft[1].get_motor_angle()]
        return [-shaft_angle[0] + shaft_angle[1], shaft_angle[0] + shaft_angle[1]]

    def move_dir(self, direction: interface.RotatorDir, speed):
        if speed > 20:
            speed = 20
        if speed < 0:
            speed = 0
        if direction == interface.RotatorDir.up:
            self.shaft[0].drive(driver.hBridge.MotorDir.clockwise, speed)
            self.shaft[1].drive(driver.hBridge.MotorDir.clockwise, speed)
        elif direction == interface.RotatorDir.down:
            self.shaft[0].drive(driver.hBridge.MotorDir.counterclockwise, speed)
            self.shaft[1].drive(driver.hBridge.MotorDir.counterclockwise, speed)
        elif direction == interface.RotatorDir.clockwise:
            self.shaft[0].drive(driver.hBridge.MotorDir.counterclockwise, speed)
            self.shaft[1].drive(driver.hBridge.MotorDir.clockwise, speed)
        elif direction == interface.RotatorDir.counterclockwise:
            self.shaft[0].drive(driver.hBridge.MotorDir.clockwise, speed)
            self.shaft[1].drive(driver.hBridge.MotorDir.counterclockwise, speed)

    def move_pos(self, pos: [int, int]):
        # convert azimuth, elevation to shaft pos
        desired_shaft_pos = [pos[0] - pos[1], pos[0] + pos[1]]
        motor_angle = [self.shaft[0].get_motor_angle(), self.shaft[1].get_motor_angle()]
        for idx, shaft in enumerate(self.shaft):
            distance = abs(motor_angle[idx] - desired_shaft_pos[idx])
            if distance <= 5:
                shaft.stop()
            else:
                speed = 1
                if distance > 20:
                    speed = 20
                if motor_angle[idx] < desired_shaft_pos[idx]:
                    shaft.drive(driver.hBridge.MotorDir.clockwise, speed)
                else:
                    shaft.drive(driver.hBridge.MotorDir.anticlockwise, speed)

    def print_debug(self):
        logger.info(str(self.shaft[0].get_motor_angle()) + "\t" +
                    str(self.shaft[0].get_shaft_angle()) + "\t" +
                    str(self.shaft[1].get_motor_angle()) + "\t" +
                    str(self.shaft[1].get_shaft_angle()))
