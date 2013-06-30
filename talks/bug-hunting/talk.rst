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

- Collections of stories and techniques I use and used in the past


What is a bug?
===============

- (Un)expected behaviour of a program

- Crash

- Incorrect result

- Memory leak

- Performance problem

- Categories

  * Deterministic

  * Undeterministic

  * Heisenbugs


Scenario
=========

- Big project

- Lot of code, lots of people, several years of development

- Complex relations in the source code

- VPBR (Very Precise Bug Report): "the program does not work!"

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

  - put a breakpoint and observe what happens

|pause|

* Very fast if the bug is simple

* Little chance of success if the bug is complex


General approach
=================

0. (from the Zen of Python): Refuse the temptation to guess

1. Reproduce the bug

2. Automatize the run (you are going to run it **many** times)

3. Find the smallest test case which fails. Write a test.

4. Spot the problem

5. Understand the problem

6. Fix it

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


Techniques
==========

- Refuse the temptation to guess (from the Zen of Python)

- Make it reproducible. Automatize

- Reduce the test case at minimum

- Write a test!

- print vs pdb




Contacts, Q&A
==============

- twitter: @antocuni

- Available for consultancy & training:

  * http://antocuni.eu

  * info@antocuni.eu

- Any question?
