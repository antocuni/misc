const fs = require('fs');

let globalWasmModule;

function print_int(n) {
    console.log(n);
}

function print_str(ptr) {
    // this is my RAM
    const HEAPU8 = new Uint8Array(globalWasmModule.instance.exports.memory.buffer);
    let s = "";

    while(1) {
        const val = HEAPU8[ptr];
        if (val == 0)
            break;
        s += String.fromCharCode(val);
        ptr++;
    }
    console.log(s);
}

const myImports = {
    env: {
        print_int,
        print_str
    }
};

const wasmBuffer = fs.readFileSync('counter.wasm');
WebAssembly.instantiate(wasmBuffer, myImports).then(wasmModule => {
  globalWasmModule = wasmModule;
  const { counter } = wasmModule.instance.exports;
  counter(10);
});
