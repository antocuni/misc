#!/usr/bin/env python

import sys
import errno
from time import time
from mplayer import mplayer, view
from math import sqrt
import array
import v0, v1, v2, v3

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
        #out = v0.sobel(img)
        #out = v1.sobel(img)
        #out = v2.sobel(img)
        out = v3.sobel(img)

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
