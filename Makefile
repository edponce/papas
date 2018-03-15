PKGDIR =  papas
TESTSDIR = tests
DOCDIR = docs


.PHONY: help clean clean_doc clean_all wheel

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to remove build, cached, compiled, and temporary package files"
	@echo "  clean_doc  to remove documentation files"
	@echo "  clean_all  to remove coverage files (in addition to clean and clean_doc)"
	@echo "  docs       to make standalone HTML files, and LaTeX files (pdflatex)"
	@echo "  build      to make package distribution"
	@echo "  wheel      to make wheel binary distribution"

clean:
	rm -rf .tox .pytest_cache
	rm -rf build dist .eggs *.egg-info
	rm -rf $(PKGDIR)/__pycache__ $(PKGDIR)/*.pyc $(PKGDIR)/*.pyo
	rm -rf $(TESTSDIR)/__pycache__ $(TESTSDIR)/*.pyc $(PKGDIR)/*.pyo

clean_doc:
	$(MAKE) -C $(DOCDIR) clean

clean_all: clean clean_doc
	rm -rf htmlcov .coverage*

docs:
	$(MAKE) -C $(DOCDIR) html
	$(MAKE) -C $(DOCDIR) latexpdf

build:
	python3 setup.py build

wheel:
	python3 setup.py bdist_wheel
