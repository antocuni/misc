#!/usr/bin/env python

import sys
import errno
from time import time
from mplayer import mplayer, view
from image import Image
from math import sqrt
import array

def sobel_magnitude(img):
    res = img.clone()
    for p in img.pixeliter():
        dx = -1.0 * img[p + (-1,-1)] + 1.0 * img[p + (1,-1)] + \
             -2.0 * img[p + (-1, 0)] + 2.0 * img[p + (1, 0)] + \
             -1.0 * img[p + (-1, 1)] + 1.0 * img[p + (1, 1)]
        dy = -1.0*img[p + (-1,-1)] -2.0*img[p + (0,-1)] -1.0*img[p + (1,-1)] + \
              1.0*img[p + (-1, 1)] +2.0*img[p + (0, 1)] +1.0*img[p + (1, 1)]
        res[p] = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
    return res

def main(argv):
    if len(argv) > 1:
        fn = argv[1]
    else:
        fn = 'test.avi -benchmark' #+ ' -vf scale=640:480'

    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    start = start0 = time()
    for fcnt, img in enumerate(mplayer(fn)):
        ## v0
        out = sobel_v0(img)
        out = Image(*out)

        ## v2
        ## img = Image(*img)
        ## out = sobel_magnitude(img)

        try:
            view(out)
        except IOError, e:
            if e.errno != errno.EPIPE:
                raise
            print 'Exiting'
            break

        print 1.0 / (time() - start), 'fps, ', (fcnt-2) / (time() - start0), 'average fps'
        start = time()
        if fcnt==2:
            start0 = time()

if __name__ == '__main__':
    main(sys.argv)