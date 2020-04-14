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

* Alternative implementations have to "emulate" CPython

* CPython can't evolve / change its details

Detail 1: refcounting
----------------------

* This is obviously backed in in the API :)

  - ``Py_INCREF``, ``Py_DECREF``, etc.

* Does not play well with GCs

* Note: the GC is **not** (only) about collecting garbage!

  - It should be called `Memory Manager`

  - A state-of-the-art GC means very fast memory allocation


Detail 2: ``PyObject *``
-------------------------

* Objects are represented by C pointers

* Implicit assumption that Python-level object identity is the same as C-level
  pointer equality

* Plays **very** bad with a moving GC


Detail 3: memory layout of structs/objects
-------------------------------------------

* C-level structs oshould be fully opaque

* Example: ``ob_type``

* Example: ``PyTypeObject``

* PEP 384 goes in the right direction


Detail 4: implicit assumptions on the implementation of data structures
-------------------------------------------------------------------------

* ``PyList_GetItem`` ==> borrowed reference

* In PyPy, lists of ints are stored as C arrays of primitive types: there is
  no reference to borrow!


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

* Massive amout of previous developer hours wasted

* Poor results

* |scriptsize| https://morepypy.blogspot.com/2018/09/inside-cpyext-why-emulating-cpython-c.html |end_scriptsize|


HPy solution
-------------

* Fully opaque data structures by default

* Higher level concepts, e.g. **handles**

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
