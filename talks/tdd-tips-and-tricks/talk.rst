.. include:: beamerdefs.txt

TDD tips tricks
================

About me
---------

- PyPy core dev since 2006

- ``pdb++``, ``cffi``, ``vmprof``, ``capnpy``, ...

- @antocuni

- http://antocuni.eu

  
About you
---------

Either:

* novice programmer

* experienced programmer but new to Python and/or TDD

    
About this talk
---------------

Two parts

* General TDD principles

* Useful patterns and tips


The goal of testing
--------------------

* Make sure that your code works

|pause|

WRONG!

The goal of testing
--------------------

* |strike<| Make sure that your code works |>|

* Make sure that your code does NOT break


Manual testing (1)
------------------

* Feature A

* Write the code

* Start the program

* Navigate through N steps

  - login

  - click on few links

  - push a button

|pause|

* CRASH!

* (repeat)

Manual testing (2)
-------------------

* Feature B

* Modify the code

* Feature B works! :-)

|pause|

* (Feature A no longer works, but you don't notice)


Automated testing (1)
-------------------------

* Write the code for Feature A

* Run a command (~0.5 secs)

  - ``py.test test_foo.py -k test_feature_A``

* CRASH

* (repeat)

Automated testing (2)
--------------------------

* Write the code for Feature B

* Run a command (~0.5 secs)

  - ``py.test test_foo.py -k test_feature_B``

* It works

|pause|

* ``py.test test_foo.py``

* CRASH

* fix

* Everyone is happy :-)


Automated testing (3)
---------------------

* What's the missing piece?

|pause|

* You have to write the test!

* It's just a program

* test frameworks/runners offer a lot of help

  - ``unittest``, ``unittest2``

  - ``nose``

  - **``py.test``**


Test Driven Development
-----------------------

* Goal: make sure that our code does not break

* What is not tested is broken (aka: Murphy's law)

* Even if it's not broken right now, it'll eventually break


Tests first
------------

* Writing code when no test is failing is **forbidden**

* You should write just the code to make the test passing

  - don't cheat :-)

* **Each test must run in isolation**

|pause|

* bonus track: VCS

  - commit every time you write/fix a test

  - write meaningful commit messages

  - don't commit if the tests are broken

  - (unless you are sure it's the right thing to do :-))

  - make you confident in your tests

  - ``{hg,git} bisect``


TDD benefits
------------

* confidence about the quality of the code

* easily spot regressions

* easily find by who/when/why a regression was introduced

* "Why the hell did I write this piece of code?"

  - look at the commit, and the corresponding test

* Remove the code, and see if/which tests fail

  - "One of my most productive days was throwing away 1000 lines of code" (Ken Thompson)

  - "Deleted code is debugged code" (Jeff Sickel)

* **The power of refactoring**


Properties of a good test
--------------------------

- It should FAIL before your fix

  - write the test first, then the code
  
- Determinism

  * NEVER write a test which fails every other run

  * pay attention e.g. to dictionary order

- Easy to READ

  * executable documentation


Readability
------------
  
* A test tells a story

* One feature per test

* Clear failures

  - When a test fails, the poor soul looking at it should be able to
    understand why

XXX example


Easy to write
-------------




GOOD PROPERTIES
easy to read
tell a story
‎ understand the logic
‎ failures should be clear
code duplication is ok

easy to write
extract common setup
‎write a test infrastructure
‎ hide boilerplate

boilerplate rule of thumb
ok to factor out init code
‎and output checking code
‎usually factor out flow control in the middle of a test is a bad idea

test multiple implementation
do: fixtures, classes, dependency injection
‎don't: for db in DBs: ...

dependency injection
show example
‎compare to monkey patching
‎
‎

Examples
--------

xxx: capnpy: test a binary blob vs nicely commented one
xxx: precomputed json vs generated one


Notation
---------

https://www.amazon.com/Practice-Programming-Addison-Wesley-Professional-Computing/dp/020161586X


Know your tools
---------------

- unittest

- unittest2

- nose

- pytest

- tox

