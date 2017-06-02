import sys
import struct
from pypytools.jitview import JitView

P1 = '\x0c\x00\x00\x00"\x00\x00\x00\x07\x00'
P2 = '\x15\x00\x00\x00+\x00\x00\x00\x08\x00'

PLIST = [P1, P2] * 2000

def read_x(p):
    return struct.unpack_from('i', p, 0)[0]

def read_y(p):
    return struct.unpack_from('i', p, 4)[0]

def read_color(p):
    return struct.unpack_from('h', p, 8)[0]

def main():
    res = 0
    for p in PLIST:
        with JitView():
            x = read_x(p)
        res += x
    print res

main()
