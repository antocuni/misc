import os, re, array
from subprocess import Popen, PIPE, STDOUT


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
        yield Image(w, h, typecode='B', fromfile=f)
        f.read(w*h/2) # Color data

class MplayerViewer(object):
    def __init__(self):
        self.width = self.height = None
    def view(self, img):
        assert img.typecode == 'B'
        if not self.width:
            w, h = img.width, img.height
            self.mplayer = Popen(['mplayer', '-', '-benchmark',
                                  '-demuxer', 'rawvideo',
                                 '-rawvideo', 'w=%d:h=%d:format=y8' % (w, h),
                                 '-really-quiet'],
                                 stdin=PIPE, stdout=PIPE, stderr=PIPE)
            
            self.width = img.width
            self.height = img.height
        assert self.width == img.width
        assert self.height == img.height
        img.tofile(self.mplayer.stdin)

default_viewer = MplayerViewer()

def view(img):
    default_viewer.view(img)
    
