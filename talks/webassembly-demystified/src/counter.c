extern void print_str(const char *message);
extern void print_int(int n);

void counter(int n) {
    print_str("Hello PyCon from WebAssembly!");
    print_str("These are some numbers:");

    for(int i=0; i<n; i++)
        print_int(i);
}
