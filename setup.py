#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


topdir = os.path.dirname(__file__)
moduledir = os.path.join(topdir, 'PaPaS')
testsdir = os.path.join(topdir, 'tests')
docdir = os.path.join(topdir, 'doc')

# Get values for package setup info from __init__.py
pkg = {}
exec(open(os.path.join(moduledir, '__init__.py')).read(), pkg)

# Load long description from file
readme = open(os.path.join(topdir, 'README.rst')).read()

requirements = [
]

setup_requirements = [
]

test_requirements = [
]

setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    author=pkg['__author__'],
    author_email=pkg['__email__'],
    maintainer=pkg['__author__'],
    maintainer_email=pkg['__email__'],
    url=pkg['__url__'],
    description=pkg['__description__'],
    long_description=readme,
    download_url=pkg['__url__'],
    keywords=pkg['__keywords__'],
    platforms='linux',
    license=pkg['__license__'],
    packages=find_packages(exclude=[docdir, testsdir]),
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
    install_requires=requirements,
    setup_requires=setup_requirements,
    test_suite=testsdir,
    tests_require=test_requirements,
)
