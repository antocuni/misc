import sys
import parser
import symbol
import pprint

def parse_and_dump(src):
    st = parser.suite(src)
    lst = st.tolist()
    lst = putsym(lst)
    pprint.pprint(lst)

def putsym(lst):
    res = []
    for item in lst:
        if isinstance(item, int):
            item = symbol.sym_name.get(item, item)
        elif isinstance(item, list):
            item = putsym(item)
        res.append(item)
    return res

parse_and_dump(sys.argv[1])
