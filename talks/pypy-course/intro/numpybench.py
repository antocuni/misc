import time

try:
    import numpypy as numpy
except ImportError:
    import numpy

def pyloop(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i]
    return sum

def c_loop(a):
    return numpy.sum(a)

a = numpy.zeros(10000000)

x = time.clock()
sum1 = pyloop(a)
y = time.clock()
print 'pyloop: %.4f secs' % (y-x)

x = time.clock()
sum2 = c_loop(a)
y = time.clock()
print 'c_loop: %.4f secs' % (y-x)

assert sum1 == sum2
