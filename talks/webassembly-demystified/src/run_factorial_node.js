const fs = require('fs');

const wasmBuffer = fs.readFileSync('factorial.wasm');
WebAssembly.instantiate(wasmBuffer).then(wasmModule => {
  const { factorial } = wasmModule.instance.exports;
  const res = factorial(5);
  console.log(res);
});
