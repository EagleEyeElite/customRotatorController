import driver
from .I2cHandler import I2cHandler
import Encoder


class Shaft(object):
    """
    summarises all components from 1 of 2 shafts
    includes: magnetic encoder, motor, rotary encoder
    """

    def __init__(self, channel, encoder: Encoder, h_bridge: driver.hBridge.HBridge, multiplexer: I2cHandler):
        self.hBridge = h_bridge
        self.mul = multiplexer
        self.encoder = encoder
        self.channel = channel
        self._shaft_offset = 0

    def get_motor_angle(self):
        encoder_pos = self.encoder.read()
        # Ticks vs Angle:
        # Motor: 11 pulses per rotation, per channel
        # 1 Motor rotation ≙ 44 Edges ( 1 Edge ≙ 1 software ticks), Gear ratio: 1:600
        # 360° ≙ 44*600 = 26400 software ticks
        # 1° ≙ 7,33 ticks
        return int(encoder_pos / 7.3)

    def shaft_angle(self):
        raw_angle = self.mul.get_magnetic_encoder(self.channel).get_raw_angle()
        angle = int(((float(raw_angle + self._shaft_offset) % 4096.0) / 4096.0) * 360.0)
        return angle

    def drive(self, direction: driver.hBridge.MotorDir, speed):
        self.hBridge.drive(self.channel, direction, speed)

    def stop(self):
        self.hBridge.stop_channel(self.channel)
