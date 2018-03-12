include AUTHORS.rst
include README.rst
include CONTRIBUTING.rst
include HISTORY.rst
include LICENSE

recursive-include tests *
recursive-include doc *.rst conf.py

recursive-exclude * __pycache__
recursive-exclude * *.py[cod]
