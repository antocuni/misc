.. include:: beamerdefs.txt

================================
PyPy JIT internals
================================


About this talk
----------------

* Overview of tracing JITs

* PyPy JIT

* Abstractions for free



Tracing JITs
-------------

* Interpret the program as usual

* Detect **hot** loops

* Tracing phase

  - **linear** trace

* Compiling

* Execute

  - guards to ensure correctness

* Profit :-)


Tracing JIT phases
-------------------

.. animage:: diagrams/tracing-phases-p*.pdf
   :align: center
   :scale: 100%


Tracing Example (1)
--------------------

* **Simplified**

|scriptsize|
|example<| |small| tracing.py |end_small| |>|

.. sourcecode:: python

   def fn(x, i):
        if i % 2 == 0:
            return x + 1
        else:
            return x

    def main():
        x = 0
        for i in range(2000):
            x = fn(x, i)
        print x

|end_example|
|end_scriptsize|


Tracing Example (2)
--------------------

|scriptsize|
|column1|
|example<| |small| dis.dis(fn) |end_small| |>|

.. sourcecode:: python

     0 LOAD_FAST          "i"
     3 LOAD_CONST         2
     6 BINARY_MODULO    
     7 POP_JUMP_IF_FALSE  18
    10 LOAD_FAST          "x"
    13 LOAD_CONST         42
    16 BINARY_ADD
    17 RETURN_VALUE
    18 LOAD_FAST          "x"
    21 LOAD_CONST         1
    24 BINARY_SUBTRACT
    25 RETURN_VALUE

|end_example|

|pause|

|column2|
|example<| |small| dis.dis(main) |end_small| |>|

.. sourcecode:: python

    ...
    19 FOR_ITER      21 (to 43)
    22 STORE_FAST     "i"

    25 LOAD_GLOBAL    "fn"
    28 LOAD_FAST      "x"
    31 LOAD_FAST      "i"
    34 CALL_FUNCTION  2
    37 STORE_FAST     "x"
    40 JUMP_ABSOLUTE 19
    ...

|end_example|
|end_columns|
|end_scriptsize|


Tracing example (3)
-------------------

.. animage:: diagrams/trace-p*.pdf
   :align: center
   :scale: 80%


Trace trees
---------------

.. animage:: diagrams/tracetree-p*.pdf
   :align: center
   :scale: 34%


Relevant Gambit example
------------------------

|scriptsize|
|example<| |small| optimiser_slave.py |end_small| |>|

.. sourcecode:: python

    def run(self):
        ...
        if self.pypy_jit_count == PYPY_DISABLE_JIT_AFTER_N_PROBLEMS:
            import pypyjit
            pypyjit.set_param("off")
            pypyjit.set_param(trace_eagerness=sys.maxint)
        self.pypy_jit_count += 1
        ...

|end_example|
|end_scriptsize|


PyPy JIT
---------------------

.. animage:: diagrams/architecture-p*.pdf
   :align: center
   :scale: 24%


PyPy trace example
-------------------

.. animage:: diagrams/pypytrace-p*.pdf
   :align: center
   :scale: 40%


PyPy optimizer
---------------

- intbounds

- constant folding / pure operations

- virtuals

- string optimizations

- heap (multiple get/setfield, etc)

- ffi

- unroll


Intbound optimization (1)
-------------------------

|example<| |small| intbound.py |end_small| |>|

.. sourcecode:: python

    def fn():
        i = 0
        while i < 5000:
            i += 2
        return i

|end_example|

Intbound optimization (2)
--------------------------

|scriptsize|
|column1|
|example<| |small| unoptimized |end_small| |>|

.. sourcecode:: python

    ...
    i17 = int_lt(i15, 5000)
    guard_true(i17)
    i19 = int_add_ovf(i15, 2)
    guard_no_overflow()
    ...

|end_example|

|pause|

|column2|
|example<| |small| optimized |end_small| |>|

.. sourcecode:: python

    ...
    i17 = int_lt(i15, 5000)
    guard_true(i17)
    i19 = int_add(i15, 2)
    ...

|end_example|
|end_columns|
|end_scriptsize|

|pause|

* It works **often**

* array bound checking

* intbound info propagates all over the trace


Virtuals (1)
-------------

|example<| |small| virtuals.py |end_small| |>|

.. sourcecode:: python

    def fn():
        i = 0
        while i < 5000:
            i += 2
        return i

|end_example|


Virtuals (2)
------------

|scriptsize|
|column1|
|example<| |small| unoptimized |end_small| |>|

.. sourcecode:: python

    ...
    guard_class(p0, W_IntObject)
    i1 = getfield_pure(p0, 'intval')
    i2 = int_add(i1, 2)
    p3 = new(W_IntObject)
    setfield_gc(p3, i2, 'intval')
    ...

|end_example|

|pause|

|column2|
|example<| |small| optimized |end_small| |>|

.. sourcecode:: python

    ...
    i2 = int_add(i1, 2)
    ...

|end_example|
|end_columns|
|end_scriptsize|

|pause|

* The most important optimization (TM)

* It works both inside the trace and across the loop

* It works for tons of cases

  - e.g. function frames


Constant folding (1)
---------------------

|example<| |small| constfold.py |end_small| |>|

.. sourcecode:: python

    def fn():
        i = 0
        while i < 5000:
            i += 2
        return i

|end_example|


Constant folding (2)
--------------------

|scriptsize|
|column1|
|example<| |small| unoptimized |end_small| |>|

.. sourcecode:: python

    ...
    i1 = getfield_pure(p0, 'intval')
    i2 = getfield_pure(<W_Int(2)>, 
                       'intval')
    i3 = int_add(i1, i2)
    ...

|end_example|

|pause|

|column2|
|example<| |small| optimized |end_small| |>|

.. sourcecode:: python

    ...
    i1 = getfield_pure(p0, 'intval')
    i3 = int_add(i1, 2)
    ...

|end_example|
|end_columns|
|end_scriptsize|

|pause|

* It "finishes the job"

* Works well together with other optimizations (e.g. virtuals)

* It also does "normal, boring, static" constant-folding


Out of line guards (1)
-----------------------

|example<| |small| outoflineguards.py |end_small| |>|

.. sourcecode:: python

    N = 2
    def fn():
        i = 0
        while i < 5000:
            i += N
        return i

|end_example|


Out of line guards (2)
----------------------

|scriptsize|
|column1|
|example<| |small| unoptimized |end_small| |>|

.. sourcecode:: python

    ...
    quasiimmut_field(<Cell>, 'val')
    guard_not_invalidated()
    p0 = getfield_gc(<Cell>, 'val')
    ...
    i2 = getfield_pure(p0, 'intval')
    i3 = int_add(i1, i2)

|end_example|

|pause|

|column2|
|example<| |small| optimized |end_small| |>|

.. sourcecode:: python

    ...
    guard_not_invalidated()
    ...
    i3 = int_add(i1, 2)
    ...

|end_example|
|end_columns|
|end_scriptsize|

|pause|

* Python is too dynamic, but we don't care :-)

* No overhead in assembler code

* Used a bit "everywhere"

How to look at traces (1)
-------------------------

* ``pypytools.jitview``

* useful for a quick look

* works best for few lines of code

|scriptsize|
|example<| |small| jitview_example.py |end_small| |>|

.. sourcecode:: python

    from pypytools.jitview import JitView

    def main():
        x = 0
        for i in range(2000):
            with JitView():
                x += i
        print x 

|end_example|
|end_scriptsize|


How to look at traces (2)
-------------------------

* ``PYPYLOG``

* ``PYPYLOG=:myfile.log pypy tracing.py``

* look for ``jit-log-opt-*`` sections


How to look at traces (3)
-------------------------

* ``vmprof``

* ``pypy -m vmprof --jitlog -o myfile.vmprof tracing.py``

* ``pypy -m vmprof.upload myfile.vmprof``

* http://vmprof.com/#/18330299-15fd-4a55-9465-9efd85fb66b1/traces


Guards
-------

- guard_true

- guard_false

- guard_class

- guard_no_overflow

- **guard_value**


Promotion
---------

- guard_value

- specialize code

- make sure not to **overspecialize**

- example: type of objects

- example: function code objects, ...


Specialization (1)
-------------------

- ``obj.foo()``

- which code is executed? (SIMPLIFIED)

  * lookup ``foo`` in obj.__dict__

  * lookup ``foo`` in obj.__class__

  * lookup ``foo`` in obj.__bases__[0], etc.

  * finally, execute ``foo``

- Precompute the lookup


Specialization (2)
--------------------

- pretend and assume that ``obj.__class__`` IS constant

  * "promotion"

  * guard_value

- now we can directly jump to ``foo`` code

  * ...unless ``foo`` is in ``obj.__dict__``: GUARD!

  * ...unless ``foo.__class__.__dict__`` changed: GUARD!

- Too many guard failures?

  * Compile some more assembler!

- guards are cheap

  * out-of-line guards even more


Specialization (3)
---------------------

- who decides what to promote/specialize for?

  * we, the PyPy devs :)

  * heuristics

- instance attributes are never promoted

- class attributes are promoted by default (with some exceptions)

- module attributes (i.e., globals) as well

- bytecode constants


Specialization trade-offs
--------------------------

- Too much specialization

  * guards fails often

  * explosion of assembler

- Not enough specialization

  * inefficient code


More about vmprof
-----------------

* Sampling profiler, low overhead (~5-10%)

* Works on CPython and PyPy

* JIT-friendly: it does not screw up relative performances

* Profiling of native code (e.g. numpy functions)

* Memory profiler

  - however the GUI seems not to work right now?

* Lots of interest

  - JetBrains sponsored native profiling and wrote their own GUI


Abstractions for free
----------------------

* Think virtual

* Temporary objects are optimized away

* Better APIs with no performance penalty

* (ab)use class and module dictionaries to drive specialization


Example
--------

- Real world example

- Decoding binary messages

- Messages: strings of bytes

|small|
|example<| |small| Point |end_small| |>|

.. sourcecode:: C

    struct Point {
        int x;
        int y;
        short color;
    }

|end_example|
|end_small|



Example: low-level solution
----------------------------

|scriptsize|
|example<| |small| decode0.py |end_small| |>|

.. sourcecode:: python

    P1 = '\x0c\x00\x00\x00"\x00\x00\x00\x07\x00\x00\x00'
    P2 = '\x15\x00\x00\x00+\x00\x00\x00\x08\x00\x00\x00'
    
    PLIST = [P1, P2] * 2000
    
    def read_x(p):
        return struct.unpack_from('i', p, 0)[0]
    
    def main():
        res = 0
        for p in PLIST:
            x = read_x(p)
            res += x
        print res

|end_example|
|end_scriptsize|


Example: better API
---------------------

|scriptsize|
|example<| |small| decode1.py |end_small| |>|

.. sourcecode:: python

    class Field(object):
        def __init__(self, fmt, offset):
            self.fmt = fmt; self.offset = offset

    class Message(object): 
       def __init__(self, name, fields):
            self._name = name; self._fields = fields
    
        def read(self, buf, name):
            f = self._fields[name]
            return struct.unpack_from(f.fmt, buf, f.offset)[0]

    Point = Message('Point', {'x': Field('i', 0), 
                              'y': Field('i', 8),
                              'color': Field('h', 16)})

    def main():
        res = 0
        for p in PLIST:
            x = Point.read(p, 'x')
            res += x
        print res

|end_example|
|end_scriptsize|


Example: faster API
---------------------

|scriptsize|
|example<| |small| decode2.py |end_small| |>|

.. sourcecode:: python

    def Message(name, fields):
        class M(object):
            def read(self, buf, name):
                f = getattr(self, name)
                return struct.unpack_from(f.fmt, buf, f.offset)[0]            
    
        for fname, f in fields.iteritems():
            setattr(M, fname, f)
    
        M.__name__ = name
        return M()
    
    Point = Message('Point', {
        'x': Field('i', 0),
        'y': Field('i', 4),
        'color': Field('h', 8)
        })
    
     ...
     x = Point.read(p, 'x')
     ...

|end_example|
|end_scriptsize|


What happened?
---------------

- dict lookups inside classes are specialized

- decode1.py

  * ``fields`` is "normal data" and expected to change

  * one JIT code for **all** possible messages

- decode2.py

  * ``fields`` is expected to be constant

  * one JIT code for **each** message

- Behaviour is the same, different performance


Example: even better API :)
-----------------------------

|scriptsize|
|example<| |small| decode3.py |end_small| |>|

.. sourcecode:: python

    class Field(object):
        def __init__(self, fmt, offset):
            self.fmt = fmt
            self.offset = offset
    
        def __get__(self, obj, cls):
            return struct.unpack_from(self.fmt, obj._buf, self.offset)[0]
    
    class Point(object):
        def __init__(self, buf):
            self._buf = buf
    
        x = Field('i', 0)
        y = Field('i', 4)
        color = Field('h', 8)
    
    def main():
        res = 0
        for p in PLIST:
            p = Point(p)
            res += p.x
        print res

|end_example|
|end_scriptsize|


Conclusion
-----------

- PyPy is cool :-)

- Any question?
