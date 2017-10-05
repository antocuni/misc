import subprocess

# BAD
def test_call_pypy_1(tmpdir):
    src = """if 1:
    def factorial(n):
        if n in (0, 1):
            return 1
        return n * factorial(n-1)

    import sys
    n = eval(sys.argv[1])
    print factorial(n)
    """
    pyfile = tmpdir.join("x.py")
    pyfile.write(src)
    stdout = subprocess.check_output(
        ["pypy", str(pyfile), "5"])
    res = eval(stdout)
    assert res == 2*3*4*5

# slightly better
def execute(tmpdir, src, *args):
    pyfile = tmpdir.join("x.py")
    pyfile.write(src)
    args = ["pypy", str(pyfile)] + list(args)
    stdout = subprocess.check_output(args)
    return eval(stdout)

def test_call_pypy_2(tmpdir):
    src = """if 1:
    def factorial(n):
        if n in (0, 1):
            return 1
        return n * factorial(n-1)

    import sys
    n = eval(sys.argv[1])
    print factorial(n)
    """
    res = execute(tmpdir, src, "5")
    assert res == 2*3*4*5

# good

import pytest
import inspect
import textwrap

@pytest.mark.usefixtures('initargs')
class PyPyTest(object):

    @pytest.fixture
    def initargs(self, tmpdir):
        self.tmpdir = tmpdir

    def run(self, fn, *args):
        fnsrc = textwrap.dedent(inspect.getsource(fn))
        boilerplate = textwrap.dedent("""
        import sys
        args = map(eval, sys.argv[1:])
        print {fnname}(*args)
        """).format(fnname=fn.__name__)
        src = fnsrc + boilerplate
        args = map(str, args)
        return execute(self.tmpdir, src, *args)

class TestCall(PyPyTest):

    def test_call(self):
        def factorial(n):
            if n in (0, 1):
                return 1
            return n * factorial(n-1)
        #
        res = self.run(factorial, 5)
        assert res == 2*3*4*5
