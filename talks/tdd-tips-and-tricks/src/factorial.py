def factorial(n):
    if n in (0, 1):
        return 1
    return n * factorial(n-1)

# DONT
def test_factorial_1():
    assert factorial(5) == 120
    assert factorial(7) == 5040

# DONT
def test_factorial_2():
    for n in (5, 7):
        res = 1
        for i in range(1, n+1):
            res *= i
        assert factorial(n) == res

# DO
def test_factorial_3():
    assert factorial(5) == 1 * 2 * 3 * 4 * 5
    assert factorial(7) == 1 * 2 * 3 * 4 * 5 * 6 * 7

