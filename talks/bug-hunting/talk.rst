.. include:: beamerdefs.txt

================================
Bug Hunting for Dummies
================================

About me
=========

- PyPy core dev

- ``pdb++``, ``fancycompleter``, ...

- Consultant, trainer

- http://antocuni.eu


About this talk
====================

    If debugging is the process of removing bugs, then programming must
    be the process of putting them in.

    (Dykstra's Observation)

|pause|

- 80% of development is spent in debugging

- 80% of debugging is spent in **finding** the bugs

  * Bug hunting!

|pause|

- No silver bullet

- The mindset of the bug hunter

- Examples of techniques I use


What is a bug?
===============

- (Un)expected behaviour of a program

  * Crash

  * Incorrect result
  
  * Memory leak

  * Performance problem

|pause|

- Categories

  * Deterministic

  * Undeterministic

  * Heisenbugs


Scenario
=========

- Big project

- Lot of code, lots of people, several years of development

- Complex relations in the source code (e.g. PyPy :))

- VPBR (Very Precise Bug Report)

  * `"the program does not work!"`

|pause|

- "Big", "lot" and "complex" are subjective

- There will always be a level of complexity which you can't understand
  immediately.

Simple approach
================

* Guess where is the problem

* Locate the related source code

* Repeat:

  - try to understand the mess of the source code

  - (optional: inspect in a debugger)

  - fix&try

|pause|

* Very fast if the bug is simple

* Little chance of success if the bug is complex

  - The world stop to make any sense

Mindset
=======

- There MUST be an explanation

- No divinity or god is against you

- Your assumptions might be wrong

- The compiler/library/O.S. is probably correct |pause|

  * Unless it's not :)




General approach
=================

|small|

(not necessarily in this order)

0. (from the Zen of Python): Refuse the temptation to guess

1. Reproduce the bug

2. Automatize the run (you are going to run it **many** times)

3. Find the smallest test case which fails. Write a test.

4. Spot the problem

5. Understand the problem

6. Fix it

|end_small|

- Goal: Understand, **then** fix



1. Reproduce the bug
=====================

- Might be tricky sometimes

- Try to reproduce it locally

  * "but it works on my machine!"

|pause|

- Pay attention to all the possible variables

  * Operating System

  * Version of program&libraries

  * CPU, 32/64 bit

  * Workload, RAM size

  * Network latency/bandwith

  * Phase of the moon

  * ..., plus any combination of the above


2. Automation
===============

- "One click away bugs"

- Avoid manual input from the user

- Example: GUI with a "load" button

  * --> small program to call the event handler directly

- Example: web application

  * --> small program which sends the "right" HTTP requests

- At worst: mouse automation (autopy, pywinauto)


3. Reduction
=============

- Goal: smallest possible program which still fail

- Example: crash in an HTML parser

- Reduce the data

  * Remove some of the tags of the offending HTML document

  * Check whether it still fails

  * Repeat

- Reduce the code

  * Remove the code for handling malformed HTML

  * If it still fails, the problem is somewhere else

  * If it stops failing, the problem is there 

- Write a test!

4. Spot the problem
========================

- Bigger reduction --> easier hunting

- If it's still too complex

  - step by step in a debugger

  - print/logging/tracing

5-6. Understand & fix
=====================

- Refuse the temptation to guess

- Fix only **after** you understood the problem

- **Write a test**

  * Almost for free once you have reduced&automated

  * Fail before, pass after the fix


Real world example
===================

- PyPy ``_fastjson`` decoder

- "Large" document crashes in the middle

- "Simple&fast" approach

  * Locate the error message

  * Look around, put a pdb, try to guess

  * No way

|pause|

- "General approach"

  * Reduce the data!

  * Write a test

  * (fix)

Useful tools
============

- Debuggers:

  - ``pdb``, ``pdb++``, ``pudb``, ``ipdb``

  - IDE debuggers (PyCharm, Wing IDE, etc.)

- Breakpoints

  - ``import pdb;pdb.set_trace()``


Post-mortem debugging
======================

- ``py.test --pdb test_myprogram.py``

- ``python -m pdb myprogram.py``

|small|
|example<| Automatic post-mortem pdb |>|

.. sourcecode:: python

    import sys
    import traceback
    import pdb

    def start_pdb(type, value, tb):
        traceback.print_exception(type, value, tb)
        print
        pdb.pm()

    sys.excepthook = start_pdb

|end_example|
|end_small|

Techniques
==========

- print vs pdb

- import pdb;pdb.xpm()

- patch open/sys.stdout

- __setattr__

- non-deterministic

- heisenbugs




Contacts, Q&A
==============

- twitter: @antocuni

- Available for consultancy & training:

  * http://antocuni.eu

  * info@antocuni.eu

- Any question?
