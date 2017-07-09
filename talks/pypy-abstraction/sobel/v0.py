import array
from math import sqrt

def sobel(img):
    """
    Low-level version: no abstractions at all
    """
    w, h, data = img
    data_out = array.array('B', [0]) * (w*h)
    out = w, h, data_out
    for y in xrange(1, h-1):
        for x in xrange(1, w-1):
            dx = (-1.0 * data[(x-1) + w*(y-1)] +
                   1.0 * data[(x+1) + w*(y-1)] +
                  -2.0 * data[(x-1) + w*y    ] +
                   2.0 * data[(x+1) + w*y    ] +
                  -1.0 * data[(x-1) + w*(y+1)] +
                   1.0 * data[(x+1) + w*(y+1)])
            #
            dy = (-1.0 * data[(x-1) + w*(y-1)] +
                  -2.0 * data[x     + w*(y-1)] +
                  -1.0 * data[(x+1) + w*(y-1)] +
                   1.0 * data[(x-1) + w*(y+1)] +
                   2.0 * data[x     + w*(y+1)] +
                   1.0 * data[(x+1) + w*(y+1)])
            #
            value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
            data_out[x + w*y] = value
    return out
