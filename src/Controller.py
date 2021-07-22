from i2cHandler import I2cHandler
from driver.hBridge import HBridge, MotorDir
from shaft import Shaft
from driver.encoder import set_up_encoder
from driver.switch import Switch
from configuration import Configuration
import time
import threading
import RPi.GPIO as GPIO


class Controller(threading.Thread):
    def __init__(self, rc: Configuration):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        ens = set_up_encoder()
        h = HBridge()
        i2c = I2cHandler()
        self.shaft = [Shaft(0, ens[0], h, i2c), Shaft(1, ens[1], h, i2c)]
        self.sw = Switch()

        self.rc = rc

    def run(self):
        while True:
            magnetic_encoder_angle = [self.shaft[0].get_magnetic_encoder_angle(), self.shaft[1].get_magnetic_encoder_angle()]
            self.rc.magnetic_encoder_angle = magnetic_encoder_angle
            encoder_pos = [self.shaft[0].encoder.read(), self.shaft[1].encoder.read()]
            self.rc.set_actual_pos(encoder_pos)
            desired_pos = self.rc.get_desired_pos()

            for idx, shaft in enumerate(self.shaft):
                if abs(encoder_pos[idx] - desired_pos[idx]) >= 100:
                    if encoder_pos[idx] < desired_pos[idx]:
                        shaft.drive(MotorDir.clockwise, 20)
                    else:
                        shaft.drive(MotorDir.anticlockwise, 20)
                else:
                    shaft.stop()

            time.sleep(0.1)
