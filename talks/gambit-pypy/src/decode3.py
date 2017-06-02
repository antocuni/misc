import sys
import struct
from pypytools.jitview import JitView

P1 = '\x0c\x00\x00\x00"\x00\x00\x00\x07\x00'
P2 = '\x15\x00\x00\x00+\x00\x00\x00\x08\x00'

PLIST = [P1, P2] * 2000

class Field(object):
    def __init__(self, fmt, offset):
        self.fmt = fmt
        self.offset = offset

    def __get__(self, obj, cls):
        return struct.unpack_from(self.fmt, obj._buf, self.offset)[0]

class Point(object):
    def __init__(self, buf):
        self._buf = buf

    x = Field('l', 0)
    y = Field('l', 4)
    color = Field('h', 8)

def main():
    res = 0
    for p in PLIST:
        with JitView():
            p = Point(p)
            res += p.x
    print res

main()
