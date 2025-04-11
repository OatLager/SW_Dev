# MAVLink CRC-16/MCRF4XX code

from builtins import object

class x25crc(object):

    def __init__(self, buf=None):
        self.crc = 0xFFFF
        if buf is not None:
            self.accumulate(buf)

    def accumulate(self, buf):
        if type(buf) is str:
            buf = buf.encode()

        accum = self.crc
        for b in buf:
            tmp = b ^ (accum & 0xFF)
            tmp = (tmp ^ (tmp << 4)) & 0xFF
            accum = (accum >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)
        self.crc = accum

    def accumulate_str(self, buf):
        return self.accumulate(buf)
