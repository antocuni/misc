from wasmtime import Store, Module, Instance

store = Store()
module = Module.from_file(store.engine, 'factorial.wasm')
instance = Instance(store, module, [])
factorial = instance.exports(store)['factorial']

print("factorial(5) =",  factorial(store, 5))
