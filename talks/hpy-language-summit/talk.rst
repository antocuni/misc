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

* Related work:

  - Stable ABI, PEP 384

  - |scriptsize| https://pythoncapi.readthedocs.io/ |end_scriptsize|

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

* ``HPyContext`` passed everywhere (useful for subinterpreters, etc.)


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


HPy targets
-----------

.. image:: img/hpy.pdf
   :scale: 50%
   :align: center


CPython ABI
-----------

|scriptsize|

.. sourcecode:: c

   // hpy/cpython.h

   typedef struct { PyObject *_o; } HPy;

   static inline HPy HPy_Dup(HPyContext ctx, HPy handle) {
       Py_XINCREF(handle._o);
       return handle;
   }

   static inline HPy HPyLong_FromLong(HPyContext ctx, long v)
   {
       return (HPy){PyLong_FromLong(v)};
   }

|end_scriptsize|


Universal ABI
--------------

|scriptsize|

.. sourcecode:: c

   // hpy/universal.h

   /* a word-sized opaque field: can be an index, a pointer, whatever */
   typedef struct { HPy_ssize_t _i; } HPy;

   struct _HPyContext_s {
       int ctx_version;
       ...
       HPy (*ctx_Dup)(HPyContext ctx, HPy h);
       HPy (*ctx_Long_FromLong)(HPyContext ctx, long value);
       ...
   };
   typedef struct _HPyContext_s *HPyContext;

   static inline HPy HPy_Dup(HPyContext ctx, HPy h) {
        return ctx->ctx_Dup ( ctx, h );
   }

   static inline HPy HPyLong_FromLong(HPyContext ctx, long value) {
        return ctx->ctx_Long_FromLong ( ctx, value );
   }

|end_scriptsize|


Implementation on PyPy
-----------------------

|scriptsize|

.. sourcecode:: python

   # pseudocode

   class HandleManager:
       def __init__(self):
           # GC-managed! The items inside the list might move in memory
           self.handles_w = []
       def new(self, w_obj):
           i = self._find_empty_index()
           self.handles_w[i] = w_obj
           return i
       ...

   def ctx_Long_FromLong(space, value):
       w_obj = space.newint(value)
       return handle_manager.new(w_obj)

   def make_context():
       ctx = lltype.malloc(HPyContext)
       ctx.ctx_Long_FromLong = ctx_Long_FromLong
       ...
       return ctx

|end_scriptsize|


Current status
---------------

* No type objects yet (WIP)

* Produce native CPython and HPy Universal extensions

* ultrajson-hpy

  - CPython ABI: as fast as ultrajson

  - Universal ABI on CPython: 10% slower

  - Universal ABI on PyPy: 3x faster

  - |scriptsize| https://github.com/pyhandle/ultrajson-hpy |end_scriptsize|

* The current approach works on the technical level

* The biggest challenge will be adoption

  - Speed on PyPy might be the most important driving force in the short term

Next steps
-----------

* Short term

    - Custom types in C

    - Validate the approach by porting PicoNumpy

      - |scriptsize| https://github.com/paugier/piconumpy |end_scriptsize|

    - Debug mode

* Medium term

  - Cython backend

  - Experiment with the real numpy

* Long term

  - PEP

  - Official PSF/CPython endorsement?
