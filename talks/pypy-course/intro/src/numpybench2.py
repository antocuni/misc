import time

try:
    import numpypy as numpy
except ImportError:
    import numpy

def pyloop(a, b, c):
    N = len(a)
    assert N == len(b) == len(c)
    res = numpy.zeros(N)
    for i in range(N):
        res[i] = a[i] + b[i]*c[i]
    return res

def c_loop(a, b, c):
    return numpy.add(a, numpy.multiply(b, c))

a = numpy.zeros(10000000)
b = numpy.ones(10000000)
c = numpy.ones(10000000)

x = time.clock()
res1 = pyloop(a, b, c)
y = time.clock()
print 'pyloop: %.4f secs' % (y-x)

x = time.clock()
res2 = c_loop(a, b, c)
y = time.clock()
print 'c_loop: %.4f secs' % (y-x)

assert (res1 == res2).all()
