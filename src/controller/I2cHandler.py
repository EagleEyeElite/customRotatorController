import driver


class I2cHandler(object):
    """
    the Handler abstracts the interface of the magnetic encoder
    the class automatically switches the multiplexer
    """

    def __init__(self):
        self._mul = driver.i2cMultiplexer.I2cMultiplexer()
        self._mEnc = [driver.magneticEncoder.MagneticEncoder(), driver.magneticEncoder.MagneticEncoder()]

    def get_magnetic_encoder(self, channel):
        """
        :param channel: select chip
        :return: correct magnetic encoder
        """
        if self._mul.channel != channel:
            self._mul.select_channel(channel)
        return self._mEnc[channel]
