PKGNAME = PaPaS
PKGDIR = src
TESTSDIR = tests
DOCDIR = doc


.PHONY:  all clean clean_all docs wheel

all:
	@echo "Under construction"

clean:
	@rm -rf .tox .pytest_cache
	@rm -rf build dist .eggs $(PKGNAME).egg-info
	@rm -rf $(PKGDIR)/__pycache__
	@rm -rf $(TESTSDIR)/__pycache__

clean_all: clean
	$(MAKE) -C $(DOCDIR) clean

docs:
	$(MAKE) -C $(DOCDIR) html
	$(MAKE) -C $(DOCDIR) latexpdf

build:
	@python3 setup.py build

wheel:
	@python3 setup.py bdist_wheel
