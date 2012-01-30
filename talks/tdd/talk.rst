.. include:: beamerdefs.txt

TDD explained
=============

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

* Goal: make sure that our code works well :-)

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

  - **never** commit if the tests are broken

  - (unless you are sure it's the right thing to do :-))

  - make you confident in your tests

  - ``hg bisect``


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


Writing tests
--------------

* Unit tests

  - better, more precise, faster

  - each piece of code in isolation

  - very (?) easy to fix is a test breaks

|pause|

* Integration tests

  - more layers of code working togheter

  - it's closer to what the final user will use and see

  - easier to write, especially for existing code

  - slower

|pause|

* Ideally, you write both

* ... but either one is better than no test :-)


Decoupling the components
-------------------------

::
    import my_database

    class Person(object):
        ...
        
        def save(self):
            if self.age < 18:
                raise TooYoungException
            my_database.insert_into('Persons', [self.name, self.age])

* ``Person`` and ``my_database`` are tightly coupled

* how can we unit-test ``save``?


Mock objects
------------

* Same interface as the "real" object

* does as little as possible

::

    class MyFakeDatabase(object):

        def __init__(self):
            self.persons = []

        def insert_into(self, tablename, values):
            if tablename == 'Persons':
                self.persons.append(values)
            else:
                assert False, 'Unkown table name: %s' % tablename

    def test_foobar():
        db = MyFakeDatabase()
        db.insert_into('Persons', ('pippo', 29))
        db.insert_into('Persons', ('topolino', 32))
        #
        assert db.persons == [
            ('pippo', 29),
            ('topolino, 32),
            ]


Dependency injection
--------------------

* Decouple ``Person`` from ``my_database``

* Goal: have a ``Person`` which uses our ``MyFakeDatabase``

* (manually editing the code is not an option :-)


Template method (1)
-------------------

- Well known design pattern

- move part of the logic in a small method

- subclasses can override it

::
    import my_database

    class Person(object):
        ...
        def get_database_module(self):
            "This is the template method!"
            return my_database

        def save(self):
            if self.age < 18:
                raise TooYoungException
            db_module = self.get_database_module()
            db_module.insert_into('Persons', [self.name, self.age])

Template method (2)
-------------------

::

    def test_Person_save():
        fake_db = MyFakeDatabase()

        class MyPerson(Person):
            def get_database_module(self):
                "Here we override the template method!"
                return fake_db

         p = MyPerson('pluto', 42)
         p.save()
         assert fake_db.persons == [
             ('pluto', 42)
             ]


Template "method" - Pythonic version
------------------------------------

* In Python, we can override also attributes::

    import my_database

    class Person(object):
        ...
        db_module = my_database  # template "attribute"

        def save(self):
            if self.age < 18:
                raise TooYoungException
            self.db_module.insert_into('Persons', [self.name, self.age])

     def test_Person_save():
         class MyPerson(Person):
             db_module = MyFakeDatabase()
         ...

Even more Pythonic
-------------------

* class declaration can contain any statement

* ``import`` is a statement::

    class Person(object):
        ...
        import my_database as db_module


Dependency injection (2)
------------------------

* Pass the dependencies "from the above"

* Don't need to create subclasses for the tests

* Often, better design::

    class Person(object):

        def __init__(self, db_module, name, age):
            self.db_module = db_module
            self.name = name
            self.age = age

        def save(self):
            if self.age < 18:
                raise TooYoungException
            self.db_module.insert_into('Persons', [self.name, self.age])


    def test_Person_save():
        fake_db = MyFakeDatabase()
         p = Person(fake_db, 'pluto', 42)
         p.save()
         assert fake_db.persons == [
             ('pluto', 42)
             ]


Monkey patching (last resort)
-----------------------------

* Useful to test existing code

* if we cannot refactor it::

    # person.py
    import my_database

    class Person(object):
        ...
        
        def save(self):
            if self.age < 18:
                raise TooYoungException
            my_database.insert_into('Persons', [self.name, self.age])

    # test_person.py
    import person

    def test_Person_save():
        fake_db = MyFakeDatabase()
        old_my_database = person.my_database
        try:
            person.my_database = fake_db
            p = Person(...)
            ...
            assert ...
        finally:
            person.my_database = old_my_database

Monkey patching (py.test magic)
--------------------------------

::

    import person

    def test_Person_save(monkeypatch):
        fake_db = MyFakeDatabase()
        # 
        monkeypatch.setattr(person, 'my_database', fake_db)
        # ^^^^^^
        p = Person(...)
        ...
        assert ...
