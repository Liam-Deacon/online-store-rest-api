# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
ifeq ($(OS),Windows_NT)
PYTHON        ?= python
else
PYTHON        ?= python3.7
endif
PACKAGE       = $(shell $(PYTHON) -W ignore -c "import sys;sys.path.insert(0, '../');import setup; print(setup.metadata['name'].replace('.', '/'))")
PACKAGE_PARENT= $(shell $(PYTHON) -W ignore -c "import os; print(os.path.dirname('$(PACKAGE)'))")
PROJECT       = $(shell $(PYTHON) -Bc 'import source.conf as sc; print(sc.project.replace(".", "-"))')
RELEASE       = $(shell $(PYTHON) -Bc 'import source.conf as sc; print(sc.project + "." + sc.release)')
PYSOURCES     = $(shell find ../$(PACKAGE) -name "*.py")
UMLOBJS       := $(pathsubst %.py,%.svg,$(PYSOURCES))
SPHINXOPTS    :=
SPHINXBUILD   = $(PYTHON) -m sphinx
SOURCEDIR     := source
BUILDDIR      := build
RTD_SERVER    :=
GRAPHVIZ_FLAGS:= -Tsvg
DOTSOURCES    := $(wildcard /source/static/*.dot)
FORCE_INPUT   = echo -e "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" |

all: cleandeps cleanuml uml licenses html htmlzip pdf epub upload


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile pd-single-pass pdf upload htmlzip all livehtml uml dependencies licenses dot cleandeps cleanuml

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

build/pdf:
	mkdir -p build/pdf

# hack as default is broken
latexpdf: build/pdf
	# The sed below is needed to ensure latexmk copes correctly with unicode greek characters
	$(MAKE) latex && sed -i -E "s|LATEXMKOPTS =|LATEXMKOPTS = -xelatex|" build/latex/Makefile && (cd build/latex/ && make) && cp build/latex/*.pdf build/pdf/

pdf-single-pass:
	 ($(FORCE_INPUT) $(MAKE) latexpdf || (cd build/latex/ && \
		$(FORCE_INPUT) latexmk -f -pdf)) && \
			cp build/latex/$(PACKAGE)*.pdf build/pdf/

# do two-pass approach to ensure bookmarks/cross-references are included in PDF output 
pdf:
	$(MAKE) pdf-single-pass
	$(MAKE) pdf-single-pass

upload:

htmlzip: html
	cd build && zip -r $(RELEASE)_rtd.zip html/ 

livehtml:
	mkdocs serve

source/uml_images:
	mkdir -p source/uml_images/

source/static:
	mkdir -p source/static

dot:
	for f in $(wildcard source/static/*.dot); do \
		echo "Converting: $$f"; \
		dot $(GRAPHVIZ_FLAGS) -O $$f; \
	done

uml: source/uml_images
	for f in `find ../$(PACKAGE) -name "[A-Za-z]*.py"`; do \
		o=$$(basename $$f | sed 's/.py//g'); $(PYTHON) -m pylint.pyreverse.main -a2 -s3 -my -f ALL -o svg -p $$o $$f; \
	done && sed -i -E "s|&#45[;]|-|g;s|[.]py||g;s|>.*$(PROJECT)/|>|g;s|^[.]||g" *.svg && mv *.svg source/uml_images/

dependencies: source/uml_images source/static
	$(PYTHON) -m pydeps --show-dot --noshow -T svg -o source/uml_images/dependencies_diagram.svg ../$(PACKAGE) > source/uml_images/dependencies_diagram.dot 
	$(PYTHON) -m pydeps --externals $(shell echo ../$(PACKAGE_PARENT)/[a-zA-Z]*) | tee source/static/dependencies.json

source/static/dependencies.json:
	$(MAKE) dependencies

source/static/licenses.rst: source/static/dependencies.json
	$(PYTHON) -m piplicenses --with-authors --with-urls --format=rst --from=source/static/dependencies.json | tee source/static/licenses.rst

licenses: source/static/licenses.rst


cleanuml:
	rm source/uml_images/classes*.svg

cleandeps:
	rm source/static/dependencies.json