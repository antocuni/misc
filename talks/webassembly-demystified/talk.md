<style>
  .reveal h1, .reveal h2, .reveal h3, .reveal h4, .reveal h5 {
    text-transform: none;
  }

  .big {
    font-size: 2.5em;
  }
</style>

## The CPU in your browser:

# WebAssembly Demystified

Antonio Cuni

PyCon DE 2023

---

## Who I am

- @antocuni

- Principal Software Engineer @ Anaconda

- Founder/Maintainer/Core dev of:

  * PyScript

  * HPy

  * PyPy

  * pdbpp++, fancycompleter, capnpy, ...

---

<span class="big fragment strike" data-fragment-index="1">Web</span><span class="big fragment strike" data-fragment-index="2">Assembly</span>

<span class="fragment" data-fragment-index="1">Not (only) for the Web</span>
<br>
<span class="fragment" data-fragment-index="2">Not an assembly (language)</span>

---

<!-- What is WebAssembly? -->
<img src="img/what-is-webassembly.png" />


---

### What is WebAssembly?

- **Virtual Machine**

- Completely sandboxed and safe

- WASM runtimes:

  * Browsers

  * node.js

  * wasmtime, wasmer, ...

- The most ubiquitous VM ever

- W3C Standard, developed by Bytecode Alliance


---

### WASM as a compilation target


- **Compilation target**: C, C++, Rust, AssemblyScript...

- Near-native performance

- Compile once, run everywhere

- != JVM or .NET: **Low Level** VM

- (but we can't call it LLVM, it's already taken)


---

<img src="img//two-hard-things.jpg" />

---

Hello World
-----------



---


WebAssembly Text Format
-----------------------

|pause|

.. image:: img/wat.jpg
   :scale: 15%
   :align: center
