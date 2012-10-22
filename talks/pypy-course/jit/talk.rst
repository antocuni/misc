.. include:: beamerdefs.txt

================================
PyPy JIT under the hood
================================

About me
---------

- PyPy core dev

- PyPy py3k tech leader

- ``pdb++``, ``fancycompleter``, ...

- Consultant, trainer

- You can hire me :-)

- http://antocuni.eu


About this talk
----------------

* What is PyPy? (in 30 seconds)

* Overview of tracing JITs

* The PyPy JIT generator


Part 0: What is PyPy?
----------------------

* RPython toolchain

  - subset of Python

  - ideal for writing VMs

  - JIT & GC for free

* Python interpreter

  - written in RPython

* Whatever (dynamic) language you want

  - smalltalk, prolog, javascript, ...


Part 1
------

**Overview of tracing JITs**

Compilers
---------

* When?

  - Batch or Ahead Of Time

  - Just In Time

|pause|

* How?

  - Static

  - Dynamic or Adaptive

|pause|

* What?

  - Method-based compiler

  - Tracing compiler

|pause|

* PyPy: JIT, Dynamic, Tracing


Assumptions
-----------

* Pareto Principle (80-20 rule)

  - the 20% of the program accounts for the 80% of the runtime

  - **hot-spots**

* Fast Path principle

  - optimize only what is necessary

  - fall back for uncommon cases

|pause|

* Most of runtime spent in **loops**

* Always the same code paths (likely)


Tracing JIT
-----------

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

.. we use java instead of RPython to avoid confusion with applevel Python


|scriptsize|
|example<| |small| java |end_small| |>|

.. sourcecode:: java

    interface Operation {
        int DoSomething(int x);
    }
    class IncrOrDecr implements Operation {
        public int DoSomething(int x) { 
            if (x < 0) return x-1;
            else       return x+1;
        }
    }
    class tracing {
        public static void main(String argv[]) {
            int N = 100;
            int i = 0;
            Operation op = new IncrOrDecr();
            while (i < N) {
                i = op.DoSomething(i);
            }
            System.out.println(i);
        }
    }

|end_example|
|end_scriptsize|


Tracing Example (2)
--------------------

|scriptsize|
|column1|
|example<| |small| Java bytecode |end_small| |>|

.. sourcecode:: java

  class IncrOrDecr {
    ...
    public DoSomething(I)I
      ILOAD 1
      IFGE LABEL_0
      ILOAD 1
      ICONST_1
      ISUB
      IRETURN
     LABEL_0
      ILOAD 1
      ICONST_1
      IADD
      IRETURN
  }

|end_example|

|pause|

|column2|
|example<| |small| Java bytecode |end_small| |>|

.. sourcecode:: java

  class tracing {
    ...
    public static main(
       [Ljava/lang/String;)V
      ...
     LABEL_0
      ILOAD 2
      ILOAD 1
      IF_ICMPGE LABEL_1
      ALOAD 3
      ILOAD 2
      INVOKEINTERFACE 
        Operation.DoSomething (I)I
      ISTORE 2
      GOTO LABEL_0
     LABEL_1
      ...
  }

|end_example|
|end_columns|
|end_scriptsize|


Tracing example (3)
-------------------

.. animage:: diagrams/trace-p*.pdf
   :align: center
   :scale: 80%


Trace trees (1)
---------------

|scriptsize|
|example<| |small| tracetree.java |end_small| |>|

.. sourcecode:: java

    public static void trace_trees() {
      int a = 0;
      int i = 0;
      int N = 100;

      while(i < N) {
        if (i%2 == 0)
            a++;
        else
            a*=2;
        i++;
      }
    }

|end_example|
|end_scriptsize|

Trace trees (2)
---------------

.. animage:: diagrams/tracetree-p*.pdf
   :align: center
   :scale: 34%


Part 2
------

**The PyPy JIT generator**

General architecture
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

* Credits to Mark Shannon

  - for the name :-)

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

Conclusion
-----------

- PyPy is cool :-)

- Any question?
