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

  * Browsers, `node.js`, `wasmtime`, `wasmer`, ...

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

<img src="img/two-hard-things.jpg" />

---

## Hello WebAssembly

```c
int factorial(int n) {
    int result = 1;

    for(int i=1; i<n+1; i++) {
        result *= i;
    }

    return result;
}
```


---

```webassembly [1-4,14-25]
(func $factorial (type $t1) (param $p0 i32) (result i32)
  (local $l1 i32) (local $l2 i32)
  (local.set $l1
    (i32.const 1))
  (if $I0
    (i32.gt_s
      (local.get $p0)
      (i32.const 0))
    (then
      (local.set $l2
        (i32.const 0))
      (local.set $l1
        (i32.const 1))
      (loop $L1
        (local.set $l1
          (i32.mul
            (local.tee $l2
              (i32.add
                (local.get $l2)
                (i32.const 1)))
            (local.get $l1)))
        (br_if $L1
          (i32.ne
            (local.get $p0)
            (local.get $l2))))))
  (local.get $l1))
```

---


### WebAssembly Text Format

<img style="max-width: 70%" class="fragment" src="img/wat.jpg" />

---

### Running WASM

- We need a **Host**

- Can be the browser, or other runtimes




---

## What can you do with WASM?

<p class="fragment">Burn a lot of CPU</p>

<p class="fragment">That's it</p>


## Safe by default
