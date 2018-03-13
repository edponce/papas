#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

# Specify main paths for package: top, src, tests
topdir = os.path.dirname(__file__)
moduledir = os.path.join(topdir, 'src')
testsdir = os.path.join(topdir, 'tests')

# Get values for package setup info from __init__.py of module
pkg = {}
with open(os.path.join(moduledir, '__init__.py'), 'r') as fd:
    exec(fd.read(), pkg)

# Load long description from file
with open(os.path.join(topdir, 'README.rst'), 'r') as fd:
    readme = fd.read()

# A list of strings specifying what other distributions need to be installed
# when this package is installed.
with open(os.path.join(topdir, 'REQUIREMENTS'), 'r') as fd:
    install_requirements = [l.strip() for l in fd.readlines()]

# A list of strings specifying what other distributions need to be present
# in order for this setup script to run.
setup_requirements = [
    'setuptools',
    'pip',
    'wheel',
]

# A list of strings specifying what other distributions need to be present
# for this package tests to run.
tests_requirements = [
]

# A dictionary mapping of names of "extra" features to lists of strings
# describing those features' requirements. These requirements will not be
# automatically installed unless another package depends on them.
extras_requirements = {
    'reST': ['Sphinx>=1.6'],
}

setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    author=pkg['__author__'],
    author_email=pkg['__author_email__'],
    maintainer=pkg['__author__'],
    maintainer_email=pkg['__author_email__'],
    url=pkg['__url__'],
    description=pkg['__description__'],
    long_description=readme,
    download_url=pkg['__url__'],
    keywords=pkg['__keywords__'],
    platforms='linux',
    license=pkg['__license__'],
    packages=find_packages(exclude=[testsdir]),
    package_dir={},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    python_requires='>=3',
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    extras_require=extras_requirements,
    test_suite=testsdir,
    tests_require=tests_requirements,
)
