"""
The most complicate ever way to produce an HTML list of fibonacci numbers
"""

def fibo():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a+b


class HtmlTag(object):
    def __init__(self, f, indent, tag):
        self.f = f
        self.tag = tag
        self.f.write(' ' * indent)
        self.f.write('<%s>' % tag)

    def __del__(self):
        self.f.write('</%s>\n' % self.tag)

def html_fibo(f):
    f.write('<ul>\n')
    try:
        for n in fibo():
            tag = HtmlTag(f, 4, 'li')
            yield n
            tag = None
    finally:
        tag = None
        f.write('</ul>\n')


def write_file():
    f = open('fibo.txt', 'w')
    for n in html_fibo(f):
        f.write('%d' % n)
        if n > 100:
            break

def main():
    write_file()
    content = open('fibo.txt').read()
    print content

if __name__ == '__main__':
    main()
