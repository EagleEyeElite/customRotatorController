import time
import RPi.GPIO as GPIO

from .I2cHandler import I2cHandler
from .Shaft import Shaft
import driver
import interface


class SatelliteReceiver(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        ens = driver.encoder.set_up_encoder()
        self.h = driver.hBridge.HBridge()
        i2c = I2cHandler()
        self.shaft = [Shaft(0, ens[0], self.h, i2c), Shaft(1, ens[1], self.h, i2c)]
        self.sw = driver.switch.Switch()

    def stop(self):
        self.shaft[0].stop()
        self.shaft[1].stop()

    def exit(self):
        self.h.set_standby(True)
        time.sleep(0.5)  # wait for motor encoder to stop
        GPIO.cleanup()

    def get_pos(self) -> [int, int]:
        motor_angle = [self.shaft[0].get_motor_angle(), self.shaft[1].get_motor_angle()]
        # TODO check if magnetic encoder
        return motor_angle

    def move_dir(self, direction: interface.RotatorDir, speed):
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
        desired_shaft_pos = self.convert_to_shaft_pos(pos)
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
        m_angle = [self.shaft[0].shaft_angle(), self.shaft[1].shaft_angle()]
        encoder_pos = [self.shaft[0].get_motor_angle(), self.shaft[1].get_motor_angle()]
        print(str(encoder_pos[0]) + "\t" +
              str(m_angle[0]) + "\t" +
              str(encoder_pos[1]) + "\t" +
              str(m_angle[1]))

        # TODO test out with actual differential

    def convert_to_coordinate(self) -> [int, int]:
        """
        :return: [azimuth, elevation]
        """
        pos = [self.shaft[0].shaft_angle(), self.shaft[1].shaft_angle()]
        return [-pos[0] + pos[1], pos[0] + pos[1]]

    def convert_to_shaft_pos(self, shaft_angle: [int, int]) -> [int, int]:
        """
        :return: [shaft0 angle, shaft1 angle]
        """
        return [shaft_angle[0] - shaft_angle[1], shaft_angle[0] + shaft_angle[1]]
