PKG = PaPaS


.PHONY:  all clean

all:
	@echo "Under construction"

clean:
	@rm -rf .tox
	@rm -rf build dist $(PKG).egg-info
