from driver.hBridge import HBridge, MotorDir
from i2cHandler import I2cHandler
import Encoder
import RPi.GPIO as GPIO


class Shaft(object):
    """
    summarises all components from 1 of 2 shafts
    includes: magnetic encoder, motor, rotary encoder
    """

    def __init__(self, channel, encoder: Encoder, h_bridge: HBridge, multiplexer: I2cHandler):
        GPIO.setmode(GPIO.BCM)
        self.hBridge = h_bridge
        self.mul = multiplexer
        self.encoder = encoder
        self.channel = channel

    def get_encoder_pos(self):
        return self.encoder.read()

    def get_magnetic_encoder_angle(self):
        return self.mul.get_magnetic_encoder(self.channel).get_raw_angle()

    def drive(self, direction: MotorDir, speed):
        self.hBridge.drive(self.channel, direction, speed)

    def stop(self):
        self.hBridge.stop_channel(self.channel)


    # TODO just some parked code, remove it if not needed
    # def angle(self, deg, dir_e):
    #     start_ticks = self._m1.encoder.read()
    #     needed_ticks = self._m1.encoder.read() + deg*((11*4*600) / 360)
    #     while self._m1.encoder.read() - needed_ticks < 15:
    #         self._m1.rotate(MotorDir.clockwise, 3000)
    #         print("ticks: {}, overall ticks: {}".format(self._m1.encoder.read() - needed_ticks, self._m1.encoder.read()))
    #
    #     self._m1.stop()
