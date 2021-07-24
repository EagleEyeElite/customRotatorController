import time
import threading
import RPi.GPIO as GPIO
import driver
import interface

from .shaft import Shaft
from .rotator import Rotator
from .i2cHandler import I2cHandler


class Controller(threading.Thread):
    def __init__(self, rc: interface.Configuration):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        ens = driver.encoder.set_up_encoder()
        h = driver.hBridge.HBridge()
        i2c = I2cHandler()
        shaft = [Shaft(0, ens[0], h, i2c), Shaft(1, ens[1], h, i2c)]
        self.Rotator = Rotator(shaft)

        self.sw = driver.switch.Switch()

        self.rc = rc
        self.m_encoder_offset = [-self.Rotator.shaft[0].get_magnetic_encoder_angle(),
                                 -self.Rotator.shaft[1].get_magnetic_encoder_angle()]

        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while True:
            if self._stop_event.is_set():
                return
            magnetic_encoder_angle = self.get_mag_encoder_angle()
            self.rc.magnetic_encoder_angle = magnetic_encoder_angle
            motor_angle = self.motor_encoder_to_angle()
            self.rc.set_actual_pos(magnetic_encoder_angle)
            desired_pos = self.rc.get_desired_pos()

            if self.rc.state == interface.State.stop:
                self.Rotator.shaft[0].stop()
                self.Rotator.shaft[1].stop()
            elif self.rc.state == interface.State.move_to_dir:
                speed = self.rc.speed
                if self.rc.get_desired_direc() == interface.RotatorDir.up:
                    self.Rotator.shaft[0].drive(driver.hBridge.MotorDir.clockwise, speed)
                    self.Rotator.shaft[1].drive(driver.hBridge.MotorDir.clockwise, speed)
                elif self.rc.get_desired_direc() == interface.RotatorDir.down:
                    self.Rotator.shaft[0].drive(driver.hBridge.MotorDir.counterclockwise, speed)
                    self.Rotator.shaft[1].drive(driver.hBridge.MotorDir.counterclockwise, speed)
                elif self.rc.get_desired_direc() == interface.RotatorDir.clockwise:
                    self.Rotator.shaft[0].drive(driver.hBridge.MotorDir.counterclockwise, speed)
                    self.Rotator.shaft[1].drive(driver.hBridge.MotorDir.clockwise, speed)
                elif self.rc.get_desired_direc() == interface.RotatorDir.counterclockwise:
                    self.Rotator.shaft[0].drive(driver.hBridge.MotorDir.clockwise, speed)
                    self.Rotator.shaft[1].drive(driver.hBridge.MotorDir.counterclockwise, speed)

            elif self.rc.state == interface.State.move_to_pos:
                desired_shaft_pos = self.convert_to_shaft_pos(desired_pos)
                for idx, shaft in enumerate(self.Rotator.shaft):
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

            time.sleep(0.1)

    def get_mag_encoder_angle(self) -> [int, int]:
        magnetic_encoder_raw_angle = [self.Rotator.shaft[0].get_magnetic_encoder_angle(),
                                      self.Rotator.shaft[1].get_magnetic_encoder_angle()]

        pos = [int(((float(magnetic_encoder_raw_angle[0] + self.m_encoder_offset[0]) % 4096.0) / 4096.0) * 360.0),
               int(((float(magnetic_encoder_raw_angle[1] + self.m_encoder_offset[1]) % 4096.0 / 4096.0)) * 360.0)]
        return pos

    def print_debug(self):
        m_angle = self.get_mag_encoder_angle()
        encoder_pos = self.motor_encoder_to_angle()
        print(str(encoder_pos[0]) + "\t" +
              str(m_angle[0]) + "\t" +
              str(encoder_pos[1]) + "\t" +
              str(m_angle[1]))

    # TODO test out with actual differential
    def convert_to_coordinate(self) -> [int, int]:
        """
        :return: [azimuth, elevation]
        """
        pos = self.get_mag_encoder_angle()
        return [-pos[0] + pos[1], pos[0] + pos[1]]

    def convert_to_shaft_pos(self, shaft_angle: [int, int]) -> [int, int]:
        """
        :return: [shaft0 angle, shaft1 angle]
        """
        return [shaft_angle[0] - shaft_angle[1], shaft_angle[0] + shaft_angle[1]]

    def motor_encoder_to_angle(self):
        encoder_pos = [self.Rotator.shaft[0].encoder.read(),
                       self.Rotator.shaft[1].encoder.read()]
        angle = [0, 0]
        # Ticks vs Angle:
        # Motor: 11 pulses per rotation, per channel
        # 1 Motor rotation ≙ 44 Edges ( 1 Edge ≙ 1 software ticks), Gear ratio: 1:600
        # 360° ≙ 44*600 = 26400 software ticks
        # 1° ≙ 7,33 ticks
        for i in range(1):
            angle[i] = int(encoder_pos[i] / 7.3)

        return angle
