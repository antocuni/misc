from pypytools.jitview import JitView

def main():
    x = 0
    for i in range(2000):
        with JitView():
            x += i
    print x

main()
