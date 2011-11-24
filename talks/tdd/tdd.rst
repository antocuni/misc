TDD explained
=============

Test Driven Development
-----------------------

* Goal: make sure that our code works well :-)

* What is not tested is broken (aka: Murphy's law)

* Even if it's not broken right now, it'll eventually break


Manual testing (1)
-----------------

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
