"""
magnetic encoder
driver module for chip AS5600,
datasheet: https://ams.com/documents/20143/36005/AS5600_DS000365_5-00.pdf
"""

from enum import IntEnum
import smbus


class AS5600(IntEnum):
    """
    defined addresses, register and bits
    datasheet: p. 5 & 6
    """
    address = 0x36
    # register
    conf = 0x07
    raw_angle = 0x0c
    status = 0x0b
    # status bits
    MH = 3
    ML = 4
    MD = 5


class MagneticEncoder(object):
    """
    magnetic encoder driver
    """

    def __init__(self):
        self.bus = smbus.SMBus(1)
        # check chip setup
        config = self.bus.read_i2c_block_data(AS5600.address, AS5600.conf, 2)
        config = int.from_bytes(config, byteorder='big')
        # check documentation page 19
        if not config == 0b00000000000000:
            raise AssertionError("AS5600: wrong config", bin(config))

    def get_raw_angle(self):
        """
        reads angle from magnetic encoder
        :return: raw angle from magnet
        """
        angle = self.bus.read_i2c_block_data(AS5600.address, AS5600.raw_angle, 2)
        angle = int.from_bytes(angle, byteorder='big')
        return angle

    def check_status(self):
        """
        checks magnet boundaries
        :raises AssertionError: magnet out of range
        """
        status = self.bus.read_i2c_block_data(AS5600.address, AS5600.status, 1)
        status = int.from_bytes(status, byteorder='big')
        if not status & (1 << AS5600.MD):
            raise AssertionError("AS5600: no magnet detected")
        if status & (1 << AS5600.ML):
            raise AssertionError("AS5600: magnet too weak")
        if status & (1 << AS5600.MH):
            raise AssertionError("AS5600: magnet too strong")
