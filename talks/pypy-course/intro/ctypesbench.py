import time
N = 10000000

def main(N):
    import ctypes
    libm = ctypes.CDLL('libm.so')
    pow = libm.pow
    pow.argtypes = [ctypes.c_double, ctypes.c_double]
    pow.restype = ctypes.c_double
    #
    i = 0
    res = 0
    start = time.clock()
    while i < N:
        res += pow(2, 3)
        i += 1
    end = time.clock()
    print 'total:', end-start
    if hasattr(pow, '_ptr'):
        print 'address:', pow._ptr.getaddr()
    return res


main(N)
