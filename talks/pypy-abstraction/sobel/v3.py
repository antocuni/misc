import itertools
import array
from collections import namedtuple
from math import sqrt
import v2

_Point = namedtuple('_Point', ['x', 'y'])
class Point(_Point):

    def __add__(self, other):
        ox, oy = other
        x = self.x + ox
        y = self.y + oy
        return self.__class__(x, y)


class ImageIter(object):

    def __init__(self, x0, x1, y0, y1):
        self.it = itertools.product(xrange(x0, x1), xrange(y0, y1))

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.it)
        return Point(x, y)


class Image(v2.Image):

    def noborder(self):
        return ImageIter(1, self.width-1, 1, self.height-1)


def sobel(img):
    img = Image(*img)
    out = Image(img.width, img.height)
    for p in img.noborder():
        dx = (-1.0 * img[p + (-1,-1)] +
               1.0 * img[p + ( 1,-1)] + 
              -2.0 * img[p + (-1, 0)] +
               2.0 * img[p + ( 1, 0)] + 
              -1.0 * img[p + (-1, 1)] +
               1.0 * img[p + ( 1, 1)])
        #
        dy = (-1.0 * img[p + (-1,-1)] +
              -2.0 * img[p + ( 0,-1)] +
              -1.0 * img[p + ( 1,-1)] + 
               1.0 * img[p + (-1, 1)] +
               2.0 * img[p + ( 0, 1)] +
               1.0 * img[p + ( 1, 1)])
        #
        value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
        out[p] = value
    return out

