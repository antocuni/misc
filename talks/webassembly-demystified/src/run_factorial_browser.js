var modPromise = WebAssembly.instantiateStreaming(
  fetch("src/factorial.wasm"), {});

async function computeFactorial() {
  const wasmModule = await modPromise;
  const { factorial } = wasmModule.instance.exports;

  const elemIn = document.getElementById('factorial-input');
  const elemOut = document.getElementById('factorial-result');
  const n = parseInt(elemIn.value);
  elemOut.innerText = factorial(n);
}
