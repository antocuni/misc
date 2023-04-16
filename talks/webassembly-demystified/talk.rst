.. include:: beamerdefs.txt

WebAssembly demystified
==============================================

.. raw:: latex

  \setbeamercovered{invisible}


Who I am
-------------

- @antocuni

- Principal Software Engineer @ Anaconda

- Founder/Maintainer/Core dev of:

  * PyScript

  * HPy

  * PyPy

  * pdbpp++, fancycompleter, capnpy, ...


What is WebAssembly?
--------------------

.. raw:: latex

  \begin{center}{\huge WebAssembly}\end{center}

  \phantom{Not (only) for the Web}

  \phantom{Not an assembly (language)}

What is WebAssembly?
--------------------

.. raw:: latex

  \begin{center}{\huge \sout{Web}Assembly}\end{center}

  Not (only) for the Web

  \phantom{Not an assembly (language)}


What is WebAssembly?
--------------------

.. raw:: latex

  \begin{center}{\huge \sout{WebAssembly}}\end{center}

  Not (only) for the Web

  Not an assembly (language)


What is WebAssembly?
--------------------

.. image:: img/what-is-webassembly.png
   :scale: 25%
   :align: center


What is WebAssembly?
--------------------

- **Virtual Machine**

- Instruction Set (ISA): i.e. a (virtual) CPU

- Completely sandboxed and safe

- WASM runtimes:

  * Browsers

  * node.js

  * wasmtime, wasmer, ...

- The most ubiquitous VM ever

- W3C Standard, developed by Bytecode Alliance


WASM as a compilation target
-----------------------------

- **Compilation target**: C, C++, Rust, AssemblyScript...

- Memory is just a big Javascript array

- Pointers are indices inside the array

- Very straightforward mapping to e.g. x86 or ARM

- Near-native performance

- Compile once, run everywhere

- Different than e.g. JVM or .NET: **Low Level** VM |pause|

- (but we can't call it LLVM, it's already taken)


Speaking of naming...
---------------------

.. image:: img/two-hard-things.jpg
   :scale: 25%
   :align: center


Hello World
-----------




WebAssembly Text Format
-----------------------

|pause|

.. image:: img/wat.jpg
   :scale: 15%
   :align: center



XXX
----


- introduction to WebAssembly
- comparison between WASM and other platforms
- WASM in the browser vs on the server
- WASI vs emscripten
- Python on WASM
- Low level details: memory, imports, exports
- Practical example of compiling/using a WASM module
- Advanced techniques: dynamic linking
- Advanced techniques: JIT compilation
- Upcoming WASM features, and why they are important:
    * Component model
    * GC integration
    * Stack switching
- WASM as a standard platform for multi language interoperability
- What are the challenges and risks for the Python community?
