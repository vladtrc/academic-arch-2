IMAGE  := ghcr.io/typst/typst:latest
SRCS   := $(wildcard src/[!_]*.typ)
PDFS   := $(patsubst src/%.typ,%.pdf,$(SRCS))
COMMON := src/_common.typ

.PHONY: all build watch clean

all: build

build: $(PDFS)

%.pdf: src/%.typ $(COMMON)
	docker run --rm -v $(CURDIR):/work -w /work $(IMAGE) compile $< $@

watch:
	docker run --rm -i \
	  -v $(CURDIR):/work \
	  -w /work \
	  alpine:3.20 sh -c \
	  'apk add --no-cache watchexec typst >/dev/null && \
	   watchexec -r -e typ -w src " \
	     for file in src/[!_]*.typ; do \
	       base=\$$(basename \$$file .typ); \
	       echo \"Compiling \$$base.typ -> \$$base.pdf\"; \
	       typst compile \$$file \$$base.pdf; \
	     done"'

clean:
	rm -f $(PDFS)
