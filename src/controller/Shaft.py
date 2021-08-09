import driver
from .I2cHandler import I2cHandler
import Encoder
from logzero import logger


class Shaft(object):
    """
    Summarises all components from 1 of 2 shafts.
    Includes: magnetic encoder, motor, rotary encoder.
    A shaft that is connected to one side of the differential is driven through a belt from a motor Shaft.
    The Angle of the differential shaft is therefore not the same as the motor angle.
    """

    def __init__(self, channel, encoder: Encoder, h_bridge: driver.hBridge.HBridge, multiplexer: I2cHandler,
                 shaft_offset):
        self.hBridge = h_bridge
        self.mul = multiplexer
        self.encoder = encoder
        self.channel = channel
        try:
            self.mul.get_magnetic_encoder(self.channel).check_status()
        except Exception as e:
            logger.info("Shaft" + str(channel) + "magnet not properly connected!" + str(e))

        # would be fixed values, when the rotator is being set up
        if shaft_offset > 4096:
            logger.info("error reading out shaft offset!!!")
        self._shaft_offset = shaft_offset
        self._motor_start_pos = self.get_shaft_angle()

    def get_shaft_angle(self):
        """
        :return: angle of shaft connected to differential (uses magnetic encoder)
        """
        raw_angle = self.mul.get_magnetic_encoder(self.channel).get_raw_angle()
        angle = int(((float(raw_angle - self._shaft_offset) % 4096.0) / 4096.0) * 360.0)
        return 360-angle

    def get_motor_angle(self):
        """
        :return: angle of motor shaft (uses quadruple encoder of motor)
        """
        encoder_pos = self.encoder.read()
        # Ticks vs Angle:
        # Motor: 11 pulses per rotation, per channel
        # 1 Motor rotation ≙ 44 Edges ( 1 Edge ≙ 1 software ticks), Gear ratio: 1:600
        # 360° ≙ 44*600 = 26400 software ticks
        # 1° ≙ 73,33 ticks
        return int(((encoder_pos / 73.33) + self._motor_start_pos))

    def drive(self, direction: driver.hBridge.MotorDir, speed):
        self.hBridge.drive(self.channel, direction, speed)

    def stop(self):
        self.hBridge.stop_channel(self.channel)
