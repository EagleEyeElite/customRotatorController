import driver
from .I2cHandler import I2cHandler
import Encoder


class Shaft(object):
    """
    summarises all components from 1 of 2 shafts
    includes: magnetic encoder, motor, rotary encoder
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
            print("Shaft", channel, "magnet not properly connected!", e)

        # TODO wil be fixed values
        if shaft_offset > 4096:
            print("error reading out shaft offset!!!")
        self._shaft_offset = shaft_offset
        self._motor_start_pos = self.get_shaft_angle()

    def get_shaft_angle(self):
        raw_angle = self.mul.get_magnetic_encoder(self.channel).get_raw_angle()
        angle = int(((float(raw_angle - self._shaft_offset) % 4096.0) / 4096.0) * 360.0)
        return 360-angle

    def get_motor_angle(self):
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
