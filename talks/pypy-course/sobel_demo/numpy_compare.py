from array import array
import math, os, re

try:
    import numpy
    import scipy.signal
    import scipy.ndimage.filters
except ImportError:
    pass
else:
    class NumpyImage(numpy.ndarray):
        def __new__(cls, a):
            return numpy.ndarray.__new__(cls, a.shape, a.dtype, a)
        @property
        def typecode(self):
            return self.dtype
        @property
        def width(self):
            return self.shape[1]
        @property
        def height(self):
            return self.shape[0]

    class NumpyNNImage(numpy.ndarray):
        def __getitem__(self, (y, x)):
            if isinstance(y, slice):
                return numpy.ndarray.__getitem__(self, (y, x))
            return numpy.ndarray.__getitem__(self, ((y + 0.5).astype(int),
                                                    (x + 0.5).astype(int)))

    class NumpyBilinImage(numpy.ndarray):
        def __getitem__(self, (y, x)):
            if isinstance(y, slice) or y.dtype==int:
                return numpy.ndarray.__getitem__(self, (y, x))
            x0, x1 = numpy.floor(x).astype(int), numpy.ceil(x).astype(int)
            y0, y1 = numpy.floor(y).astype(int), numpy.ceil(y).astype(int)
            xoff, yoff = x-x0, y-y0
            return (1.0-xoff)*(1.0-yoff) * self[y0, x0] + \
                   (    xoff)*(1.0-yoff) * self[y0, x1] + \
                   (1.0-xoff)*(    yoff) * self[y1, x0] + \
                   (    xoff)*(    yoff) * self[y1, x1]

def wrap_numpy(fn):
    def f(a):
        return NumpyImage(fn(a.ndarray()))
    return f
    
######################################################################
        
class Image(array):
    def __new__(cls, w, h, typecode='d', data=None):
        self = array.__new__(cls, typecode)
        return self
        
    def __init__(self, w, h, typecode='d', data=None):
        self.width = w
        self.height = h
        if data is None:
            self.append(0)
            self *= w*h
        elif isinstance(data, file):
            self.fromfile(data, w * h)
        else:
            self.extend(data)

    def new(self, width=None, height=None, typecode=None):
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if typecode is None:
            typecode = self.typecode
        return Image(width, height, typecode)

    def clone(self):
        return Image(self.width, self.height, self.typecode, self)
            
    def _idx(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return y*self.width + x
        raise IndexError

    def __getitem__(self, (x, y)):
        return array.__getitem__(self, self._idx(x, y))

    def __setitem__(self, (x, y), val):
        array.__setitem__(self, self._idx(x, y), val)

    def pixels(self, border=0, xborder=None, yborder=None):
        if xborder is None:
            xborder = border
        if yborder is None:
            yborder = border
        for y in xrange(border, self.height-yborder):
            for x in xrange(border, self.width-xborder):
                yield x, y

    def ndarray(self):
        return numpy.ndarray((self.height, self.width), self.typecode, self)

class ZeroPaddedImage(Image):
    def __getitem__(self, (x, y)):
        try:
            return array.__getitem__(self, self._idx(x, y))
        except IndexError:
            return 0

class NNImage(Image):
    def __getitem__(self, (x, y)):
        return Image.__getitem__(self, (int(x + 0.5), int(y + 0.5)))

    def ndarray(self):
        return NumpyNNImage((self.height, self.width), self.typecode, self)

class BilinImage(Image):
    def __getitem__(self, (x, y)):
        if isinstance(x, float) and isinstance(y, float):
            x0, x1 = int(math.floor(x)), int(math.ceil(x))
            y0, y1 = int(math.floor(y)), int(math.ceil(y))
            xoff, yoff = x-x0, y-y0
            return (1.0-xoff)*(1.0-yoff) * self[x0, y0] + \
                   (1.0-xoff)*(    yoff) * self[x0, y1] + \
                   (    xoff)*(1.0-yoff) * self[x1, y0] + \
                   (    xoff)*(    yoff) * self[x1, y1]
        else:
            return Image.__getitem__(self, (x, y))

    def ndarray(self):
        return NumpyBilinImage((self.height, self.width), self.typecode, self)

######################################################################

def sobel_magnitude(a): # pypy: 106 fps, cpython: 0.74 fps 
    b = a.new()
    for x, y in a.pixels(border=1):
        dx = -1.0 * a[x-1, y-1] + 1.0 * a[x+1, y-1] + \
             -2.0 * a[x-1, y  ] + 2.0 * a[x+1, y  ] + \
             -1.0 * a[x-1, y+1] + 1.0 * a[x+1, y+1]
        dy = -1.0 * a[x-1, y-1] - 2.0 * a[x, y-1] - 1.0 * a[x+1, y-1] + \
              1.0 * a[x-1, y+1] + 2.0 * a[x, y+1] + 1.0 * a[x+1, y+1]
        b[x, y] = min(int(math.sqrt(dx*dx + dy*dy) / 4.0), 255)
    return b

@wrap_numpy
def sobel_magnitude_numpy(a): # 38 fps
    dx = scipy.signal.convolve2d(a, numpy.array([[-1.0, 0.0, 1.0],
                                                 [-2.0, 0.0, 2.0],
                                                 [-1.0, 0.0, 1.0]]), 'same')
    dy = scipy.signal.convolve2d(a, numpy.array([[-1.0, -2.0, -1.0],
                                                 [ 0.0,  0.0,  0.0],
                                                 [ 1.0,  2.0,  1.0]]), 'same')
    return numpy.minimum(numpy.sqrt(dx*dx + dy*dy) / 4.0, 255).astype('B')

@wrap_numpy
def sobel_magnitude_numpy2(a): # 89 fps (Image), 81 fps (NNImage),  80 fps (BilinImage)
    dx = -1.0 * a[0:-3, 0:-3] + 1.0 * a[0:-3, 2:-1] + \
         -2.0 * a[1:-2, 0:-3] + 2.0 * a[1:-2, 2:-1] + \
         -1.0 * a[2:-1, 0:-3] + 1.0 * a[2:-1, 2:-1]
    dy = -1.0 * a[0:-3, 0:-3] - 2.0 * a[0:-3, 1:-2] - 1.0 * a[0:-3, 2:-1] + \
          1.0 * a[2:-1, 0:-3] + 2.0 * a[2:-1, 1:-2] + 1.0 * a[2:-1, 2:-1] 
    res = numpy.zeros(a.shape)
    res[1:-2, 1:-2] = numpy.minimum(numpy.sqrt(dx*dx + dy*dy) / 4.0, 255)
    return res.astype('B')

@wrap_numpy
def sobel_magnitude_numpy3(a): # 106 fps
    dx = numpy.zeros(a.shape)
    scipy.ndimage.filters.sobel(a, 1, dx)
    dy = numpy.zeros(a.shape)
    scipy.ndimage.filters.sobel(a, 0, dy)
    return numpy.minimum(numpy.sqrt(dx*dx + dy*dy) / 4.0, 255).astype('B')

@wrap_numpy
def sobel_magnitude_numpy4(a): # 105 fps
    dx = numpy.zeros(a.shape)
    scipy.ndimage.filters.convolve(a, numpy.array([[-1.0, 0.0, 1.0],
                                                   [-2.0, 0.0, 2.0],
                                                   [-1.0, 0.0, 1.0]]), dx)
    dy = numpy.zeros(a.shape)
    scipy.ndimage.filters.convolve(a, numpy.array([[-1.0, -2.0, -1.0],
                                                   [ 0.0,  0.0,  0.0],
                                                   [ 1.0,  2.0,  1.0]]), dy)
    return numpy.minimum(numpy.sqrt(dx*dx + dy*dy) / 4.0, 255).astype('B')

######################################################################

def magnify(img): # pypy: 86 fps, cpython: 3.4 fps (NNImage)
                  # pypy: 78 fps, cpython: 2.1 fps (BilinImage)
    out = img.clone()
    maxr = img.height/3
    for x, y in img.pixels(xborder=img.width/2 - maxr, yborder=img.height/2 - maxr):
            dx, dy = x - img.width/2, y - img.height/2
            a = math.atan2(dy, dx)
            r = math.sqrt(dx ** 2 + dy ** 2)
            if r < maxr:
                nr = r*r / maxr
                nx, ny = nr*math.cos(a), nr*math.sin(a)
                out[x,y] = min(int(img[nx + img.width/2, ny + img.height/2]), 255)
            else:
                out[x,y] = img[x,y]
    return out

@wrap_numpy
def magnify_numpy(img): # 83 fps (NNImage), 62 fps (BilinImage)
    out = img.copy()
    maxr = img.shape[0]/3
    x, y = numpy.meshgrid(range(img.shape[1]/2 - maxr, img.shape[1]/2 + maxr),
                          range(img.shape[0]/2 - maxr, img.shape[0]/2 + maxr))
    dx, dy = x - img.shape[1]/2, y - img.shape[0]/2
    a = numpy.arctan2(dy, dx)
    r = numpy.sqrt(dx ** 2 + dy ** 2)
    nr = r*r / maxr
    nx, ny = nr*numpy.cos(a) + img.shape[1]/2, nr*numpy.sin(a) + img.shape[0]/2
    outsub = out[img.shape[0]/2 - maxr : img.shape[0]/2 + maxr,
                 img.shape[1]/2 - maxr : img.shape[1]/2 + maxr]
    outsub[r<maxr] = img[ny[r<maxr], nx[r<maxr]]
    return numpy.minimum(out, 255).astype('B')

######################################################################

def range2d(a, b):
    for y in range(a, b):
        for x in range(a, b):
            yield x, y
            
def local_max(img):  # pypy: 4.72 fps, cpython: 0.31 fps 
    s = 3
    out = img.new()
    for x, y in img.pixels(border=s):
        for dx, dy in range2d(-s, s+1):
            if img[x+dx, y+dy] > img[x, y]:
                break
        else:
            out[x, y] = 255
    return out

def local_edge(img):  # pypy: 10.25 fps, cpython: 0.25 fps (including sobel_magnitude)
    out = img.new()
    for x, y in img.pixels(border=1):
        n = len([1 for dx, dy in range2d(-1, 2) if img[x+dx, y+dy] > img[x, y]])
        if n <= 3 and img[x,y] > 20:
            out[x, y] = 255
    return out

# Haar detector
# Tracing linesegments
# Subpixel edge-detection
# Distance-transform
# Subpixel correlation/edge-detection
                
######################################################################


def mplayer(Image, fn='tv://', options=''):
    f = os.popen('mplayer -really-quiet -noframedrop ' + options + ' ' 
                 '-vo yuv4mpeg:file=/dev/stdout 2>/dev/null </dev/null ' + fn)
    hdr = f.readline()
    m = re.search('W(\d+) H(\d+)', hdr)
    w, h = int(m.group(1)), int(m.group(2))
    while True:
        hdr = f.readline()
        if hdr != 'FRAME\n':
            break
        yield Image(w, h, 'B', f)
        f.read(w*h/2) # Color data

class MplayerViewer(object):
    def __init__(self):
        self.width = self.height = None
    def view(self, img):
        assert img.typecode == 'B'
        if not self.width:
            self.mplayer = os.popen('mplayer -really-quiet -noframedrop - ' +
                                    '2> /dev/null ', 'w')
            self.mplayer.write('YUV4MPEG2 W%d H%d F100:1 Ip A1:1\n' %
                               (img.width, img.height))
            self.width = img.width
            self.height = img.height
            self.color_data = array('B', [127]) * (img.width * img.height / 2)
        assert self.width == img.width
        assert self.height == img.height
        self.mplayer.write('FRAME\n')
        img.tofile(self.mplayer)
        self.color_data.tofile(self.mplayer)

default_viewer = MplayerViewer()

def view(img):
    default_viewer.view(img)
    

if __name__ == '__main__':
    from time import time

    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    start = start0 = time()
    for fcnt, img in enumerate(mplayer(BilinImage, 'test.avi', '-benchmark')):
        #view(img)
        #view(sobel_magnitude(img))
        #view(sobel_magnitude_numpy2(img))
        #view(magnify(img))
        view(magnify_numpy(img))
        #view(local_max(img))
        #view(local_edge(sobel_magnitude(img)))
        print 1.0 / (time() - start), 'fps, ', (fcnt-2) / (time() - start0), 'average fps'
        start = time()
        if fcnt==2:
            start0 = time()
