factorial.wasm: factorial.c
	clang \
		--target=wasm32 \
		-nostdlib \
		-Wl,--export-all -Wl,--no-entry, -Wl,--allow-undefined \
		-g \
		-O1 \
		-o factorial.wasm \
		factorial.c

counter.wasm: counter.c
	clang \
		--target=wasm32 \
		-nostdlib \
		-Wl,--export-all -Wl,--no-entry, -Wl,--allow-undefined \
		-g \
		-O1 \
		-o counter.wasm \
		counter.c


.PHONY: wasm2wat
wasm2wat: factorial.wasm
	wasm2wat --generate-names -f factorial.wasm | pygmentize -l wast -P style=rrt
