from wasmtime import Store, Module, Instance, Func, FuncType, ValType

store = Store()
module = Module.from_file(store.engine, 'counter.wasm')

def print_num(n):
    print(n)

def print_str(ptr):
    memory = instance.exports(store).get("memory")
    s = ""
    while True:
        val = memory.read(store, ptr, ptr+1)[0]
        if val == 0:
            break
        s += chr(val)
        ptr += 1
    print(s)

print_num_func = Func(store, FuncType([ValType.i32()], []), print_num)
print_str_func = Func(store, FuncType([ValType.i32()], []), print_str)

instance = Instance(store, module, [print_str_func, print_num_func])
counter = instance.exports(store)['counter']

counter(store, 10)
