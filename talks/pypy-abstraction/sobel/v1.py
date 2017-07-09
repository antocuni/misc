import array
from math import sqrt

def get(img, x, y):
    w, h, data = img
    i = x + y*w
    return data[i]

def set(img, x, y, value):
    w, h, data = img
    i = x + y*w
    data[i] = value

def sobel(img):
    """
    Same as v0, but with get() and set() functions
    """
    w, h, data = img
    out = w, h, array.array('B', [0]) * (w*h)
    for y in xrange(1, h-1):
        for x in xrange(1, w-1):
            dx = (-1.0 * get(img, x-1, y-1) +
                   1.0 * get(img, x+1, y-1) +
                  -2.0 * get(img, x-1, y)   +
                   2.0 * get(img, x+1, y)   +
                  -1.0 * get(img, x-1, y+1) +
                   1.0 * get(img, x+1, y+1))
            #
            dy = (-1.0 * get(img, x-1, y-1) +
                  -2.0 * get(img, x,   y-1) +
                  -1.0 * get(img, x+1, y-1) +
                   1.0 * get(img, x-1, y+1) +
                   2.0 * get(img, x,   y+1) +
                   1.0 * get(img, x+1, y+1))
            #
            value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
            set(out, x, y, value)
    return out
