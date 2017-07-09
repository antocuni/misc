import array
from math import sqrt

class Image(object):

    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height
        if data is None:
            self.data = array.array('B', [0]) * (width*height)
        else:
            self.data = data

    def __getitem__(self, idx):
        x, y = idx
        return self.data[x + y*self.width]

    def __setitem__(self, idx, value):
        x, y = idx
        self.data[x + y*self.width] = value


def sobel(img):
    """
    Wrap the image inside an Image class
    """
    img = Image(*img)
    out = Image(img.width, img.height)
    for y in xrange(1, img.height-1):
        for x in xrange(1, img.width-1):
            dx = (-1.0 * img[x-1, y-1] +
                   1.0 * img[x+1, y-1] +
                  -2.0 * img[x-1, y]   +
                   2.0 * img[x+1, y]   +
                  -1.0 * img[x-1, y+1] +
                   1.0 * img[x+1, y+1])
            #
            dy = (-1.0 * img[x-1, y-1] +
                  -2.0 * img[x,   y-1] +
                  -1.0 * img[x+1, y-1] +
                   1.0 * img[x-1, y+1] +
                   2.0 * img[x,   y+1] +
                   1.0 * img[x+1, y+1])
            #
            value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
            out[x, y] = value
    return out
