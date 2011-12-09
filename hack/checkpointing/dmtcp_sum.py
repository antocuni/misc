# simple app which computes the sum of 1..N-1, integrated with DMTCP
# checkpointing facilities to preserve the JITted code between runs.

import os

def hook(name, kind, where, ops):
    codeobj, nextinstr, is_being_profiled = where
    print '[PYPY JIT] compiling', kind, codeobj.co_name

try:
    import pypyjit
    pypyjit.set_compile_hook(hook)
except ImportError:
    print 'not on pypy, not setting compile hook'

def myfunc(N):
    res = 0
    for i in range(N):
        res += i
    return res

def main():
    x = myfunc(2000)
    print 'the result is', x


def magic_run(fn):
    import dmtcp
    i = 0
    while True:
        print 'run', i
        i += 1
        fn() # run the main program
        #res = dmtcp.checkpoint()
        res = 1
        if res == dmtcp.AFTER_CHECKPOINT:
            return

if __name__ == '__main__':
    magic_run(main)
    
