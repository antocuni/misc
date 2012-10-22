class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError
        x1 = self.x + other.x
        y1 = self.y + other.y
        return Point(x1, y1)

def main():
    p = Point(0.0, 0.0)
    while p.x < 2000.0:
        p = p + Point(1.0, 0.5)
    print p.x, p.y

main()

