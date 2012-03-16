Python White Magic
===================

Python is a powerful language.  Beginners appreciate its surface of simplicity
and ease to use, where (almost) everything "just works" (TM) as expected.
However, under the hood, there is a whole world of rules and layers which can
be (ab)used by experienced programmers to tweak the language in unexpected
ways.

Often, these techniques are labeled as "hacks" or "black magic", to indicate
that they should not used in production or that you should not look at it
unless you are "initiated" to some not better specified sorcery.

However, if used with care and in the right places, these techniques can lead
to better, faster and/or more readable code, or can be extremely useful during
debugging, and thus deserve the definition of "white magic" which programmers
can use to improve their code. Moreover, looking at how they are implemented
is a good way to learn about some of the deep corners of the language.

This talk presents some of these advanced techniques which I have seen in use
in real code, e.g. in PyPy or pdb++. Including, but not limited to: creating
new functions by reusing existing code objects, instantiating multiple copies
of the same module, playing with metaclasses in various ways, changing the
``__class__`` of an object on the fly to get specialized behavior,
automatically entering the debugger when a certain event occur, etc.

