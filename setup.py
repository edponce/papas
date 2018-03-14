#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


# Specify paths for package modules
pkgdir = 'src'
testsdir = 'tests'

# Load package info from __init__.py
pkg = {}
with open(os.path.join(pkgdir, '__init__.py'), 'r') as init:
    exec(init.read(), pkg)

# Load long description from files
with open('README.rst', 'r') as readme, open('CHANGELOG.rst', 'r') as history:
    long_description = '\n' + readme.read() + '\n\n' + history.read()

# A list of strings specifying what other distributions need to be installed
# when this package is installed.
install_requirements = [
    'PyYAML>=3.12',
    'configparser>=3.5',
    'mpi4py>=3.0',
]

# A list of strings specifying what other distributions need to be present
# in order for this setup script to run.
setup_requirements = [
    'setuptools>=38.5',
    'pip>=9.0',
    'wheel>=0.30',
]

# A list of strings specifying what other distributions need to be present
# for this package tests to run.
tests_requirements = [
    'tox>=2.9',
    'coverage>=4.5.1',
    'codecov>=2.0.15',
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
    description=pkg['__description__'],
    long_description=long_description,
    keywords=pkg['__keywords__'],
    url=pkg['__url__'],
    download_url=pkg['__url__'],
    author=pkg['__author__'],
    author_email=pkg['__author_email__'],
    license=pkg['__license__'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=['Linux'],
    zip_safe=False,
    python_requires='>=3',
    packages=find_packages(exclude=[testsdir]),
    include_package_data=True,
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    extras_require=extras_requirements,
    tests_require=tests_requirements,
    test_suite=testsdir,
)
