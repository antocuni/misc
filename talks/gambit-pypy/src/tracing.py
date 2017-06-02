def fn(x, i):
    if i % 2:
        return x + 42
    else:
        return x - 1

def main():
    x = 0
    for i in range(2000):
        x = fn(x, i)
    print x


if __name__ == '__main__':
    main()
