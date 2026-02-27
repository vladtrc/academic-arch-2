IMAGE  := ghcr.io/typst/typst:latest
SRCS   := $(wildcard src/[!_]*.typ)
PDFS   := $(patsubst src/%.typ,%.pdf,$(SRCS))
COMMON := src/_common.typ
FILE   ?= src/ais.typ
ARCH_YAML := scripts/clean-architecture.yaml
ARCH_SVG  := src/assets/clean-architecture.svg

.PHONY: all build watch clean list

ifneq (,$(filter list,$(MAKECMDGOALS)))
LIST_EXTRA := $(filter-out list,$(MAKECMDGOALS))
$(LIST_EXTRA):
	@:
endif

all: build

build: $(PDFS)

$(ARCH_SVG): scripts/gen_arch_svg.py $(ARCH_YAML) scripts/pyproject.toml
	UV_CACHE_DIR=/tmp/uv-cache uv run --no-sync --project scripts scripts/gen_arch_svg.py --input $(ARCH_YAML) --output $(ARCH_SVG)

ais.pdf: $(ARCH_SVG)

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

list:
	@target="$(FILE)"; \
	arg="$(word 2,$(MAKECMDGOALS))"; \
	if [ -n "$$arg" ]; then \
	  case "$$arg" in \
	    *.typ|*/*) target="$$arg" ;; \
	    *) target="src/$$arg.typ" ;; \
	  esac; \
	fi; \
	test -f "$$target" || (echo "File not found: $$target"; exit 1); \
	awk '\
	  /^=+ / { \
	    line = $$0; \
	    lvl = 0; \
	    while (substr(line, lvl + 1, 1) == "=") lvl++; \
	    text = line; \
	    sub(/^=+ /, "", text); \
	    sub(/ *<[^>]+>$$/, "", text); \
	    if (match(text, /#new-module\("([^"]+)"\)/, m)) { \
	      text = "Модуль: " m[1]; \
	    } else if (match(text, /#new-lecture\("([^"]+)"\)/, m)) { \
	      text = "Лекция: " m[1]; \
	    } \
	    indent = ""; \
	    for (i = 1; i < lvl; i++) indent = indent "  "; \
	    printf "%s- %s\n", indent, text; \
	  } \
	' "$$target"
