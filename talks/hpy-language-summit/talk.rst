.. include:: beamerdefs.txt

HPy: a future-proof way of extending Python?
==============================================

What is HPy?
-------------

* An attempt to "solve" some of the problems with the C-API

* Idea born at EP2019, discussion between:

  - PyPy devs

  - CPython devs

  - Cython dev(s)

* |scriptsize| https://github.com/pyhandle/hpy |end_scriptsize|

* |scriptsize| https://hpy.readthedocs.io/en/latest/ |end_scriptsize|


What is the problem?
--------------------

* The C-API is too tied to CPython internals

* Many implementation details are exposed by/backed in the API

* CPython can't evolve / change its details

* Alternative implementations have to "emulate" CPython


Exposed details
-----------------

* Reference counting

* Objects as C pointers (``PyObject *``)

  - Implicit assumption that Python-level ``is`` is the same as C-level ``==``

* Structs not fully opaque

  - ``ob_refcnt``, ``ob_type``, ``PyTypeObject``, ...

  - PEP 384 goes in the right direction

* Borrowed references

  - ``PyList_GetItem`` ==> borrowed reference

  - In PyPy, ``[1, 2, 3, 4]`` is represented as a C ``long[]``

  - No references to borrow!


Refcounting vs GC
------------------

* Refcounting prevents using a "real" GC

* The GC is **not** (only) about collecting garbage!

  - It should be called `Memory Manager`

* State-of-the-art GCs:

  - super-fast allocation, fast deallocation

  - no/minimal pauses

  - multi-threading (not the PyPy GC)

  - ...

- E.g., on `gcbench.py`_, PyPy is ~25x faster than CPython!

.. _`gcbench.py`: https://foss.heptapod.net/pypy/pypy/blob/branch/default/rpython/translator/goal/gcbench.py

CPython
--------

* Can't evolve the VM

* Can't experiment with many ideas

* Refcounting is a big problem

|small|

    Refcounting is the major blocker / problem for the Gilectomy.  The next
    step with the Gilectomy is to switch CPython to tracing garbage
    collection, which is much more amenable to running across multiple
    threads.

    Larry Hastings

|end_small|


Alternative implementations
----------------------------

* Standard solution: compatibility layer to emulate CPython

  - PyPy: cpyext

  - IronPython: IronClad

  - Jython: Jython Native Interface

  - ...

* Massive amout of precious developer hours wasted

* Poor results

* |scriptsize| https://morepypy.blogspot.com/2018/09/inside-cpyext-why-emulating-cpython-c.html |end_scriptsize|


HPy solution
-------------

* Fully opaque data structures by default

* GC-friendly: **handles**

  - Like file descriptors of Windows's ``HANDLE``

  - ``HPy_Dup`` ==> ``Py_INCREF``

  - ``HPy_Close()`` ==> ``Py_DECREF``

* Each handle must be closed individually

|scriptsize|

.. sourcecode:: c

    PyObject *a = PyLong_FromLong(42);
    PyObject *b = a;
    Py_INCREF(b);
    Py_DECREF(a);
    Py_DECREF(a); // Ok

    HPy a = HPyLong_FromLong(ctx, 42);
    HPy b = HPy_Dup(ctx, a);
    HPy_Close(a);
    HPy_Close(a); // WRONG!

|end_scriptsize|


HPy strategy to conquer the world
----------------------------------

* Zero overhead on CPython

  - Using macros and ``static inline`` to map HPy to C-API

* Incremental adoption

  - Port existing extensions one function at a time

* Faster on alternative implementations

  - 3x faster than cpyext on PyPy

  - 2x faster on GraalPython (could be optimized further)

* Better debugging experience

  - "The handle created at foo.c:543 was never closed"

* (Optional) Universal ABI: one binary for multiple versions/implementations

* Cython backend
