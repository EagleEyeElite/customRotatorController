"""
i2c multiplexer
selects one of two magnetic encoder chips
driver module for chip PCA9540B,
datasheet: https://www.nxp.com/docs/en/data-sheet/PCA9540B.pdf
"""

from enum import IntEnum
import smbus


class PCA9540B(IntEnum):
    # datasheet: p. 5 & 6
    address = 0b1110000
    # channel select
    default_state = 0b00000000
    select_channel_0 = 0b00000100
    select_channel_1 = 0b00000101


class I2cMultiplexer(object):
    """
    i2c multiplexer
    selects one of two magnetic encoder chips
    """

    def __init__(self):
        self.channel = None
        self._bus = smbus.SMBus(1)
        self._select_channel = [PCA9540B.select_channel_1, PCA9540B.select_channel_0]
        self.select_channel(0)

    def select_channel(self, channel):
        """
        selects between two connected magnetic encoders
        channel 0 is the lower, channel 1 is the upper connector on the pcb
        :param channel: channel selection
        """
        self._bus.write_byte(PCA9540B.address, self._select_channel[channel])
        self.channel = channel
