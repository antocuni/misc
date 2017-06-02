import sys
import struct

P1 = '\x0c\x00\x00\x00"\x00\x00\x00\x07\x00'
P2 = '\x15\x00\x00\x00+\x00\x00\x00\x08\x00'

PLIST = [P1, P2] * 2000

class Field(object):

    def __init__(self, fmt, offset):
        self.fmt = fmt
        self.offset = offset

def Message(name, fields):
    class M(object):
        def read(self, buf, name):
            f = getattr(self, name)
            return struct.unpack_from(f.fmt, buf, f.offset)[0]            

    for fname, f in fields.iteritems():
        setattr(M, fname, f)

    M.__name__ = name
    return M()


Point = Message('Point', {
    'x': Field('l', 0),
    'y': Field('l', 4),
    'color': Field('i', 8)
    })


def main():
    res = 0
    for p in PLIST:
        x = Point.read(p, 'x')
        res += x
    print res

main()
