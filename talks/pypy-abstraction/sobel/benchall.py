import time
import pypytools
from mplayer import mplayer
import v0, v1, v2, v3

def bench():
    if pypytools.IS_PYPY:
        max_frames = 200
    else:
        max_frames = 10

    fn = 'test.avi -benchmark'
    for v in (v0, v1, v2, v3):
        start = time.time()
        for i, img in enumerate(mplayer(fn)):
            out = v.sobel(img)
            if i == max_frames:
                break
        end = time.time()
        fps = i / (end-start)
        print '%s: %.2f fps' % (v.__name__, fps)


if __name__ == '__main__':
    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    bench()

