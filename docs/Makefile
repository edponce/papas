# Makefile for Sphinx documentation

SPHINXBUILD   = python3 -m sphinx
SPHINXPROJ    =
SOURCEDIR     = .
BUILDDIR      = _build
SPHINXOPTS    = -W


.PHONY: help clean Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo -e "  \033[01;34mclean\033[00m       to remove built documentation files"

clean:
	rm -rf "$(BUILDDIR)"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for "$(SOURCEDIR)" $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
