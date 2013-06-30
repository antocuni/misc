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


Debugging
====================

If debugging is the process of removing bugs, then programming must
be the process of putting them in.

(Dykstra's Observation)

|pause|

- 80% of development is spent in debugging

- 80% of debugging is spent in **finding** the bugs

|pause|

- No silver bullet

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

- Bug report: "the program does not work!"

|pause|

- "Big", "lot" and "complex" are subjective

- There will always be a level of complexity which you can't understand
  immediately.


General approach
=================

0. (from the Zen of Python): Refuse the temptation to guess

1. Reproduce the bug

2. Automatize the run (you are going to run it **many** times)

3. 



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
