#!/usr/bin/env python3

from setuptools import setup, find_packages
import papas


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
    'tox-travis>=0.10',
    'flake8>=3.5',
    'coverage>=4.5.1',
]

# A dictionary mapping of names of "extra" features to lists of strings
# describing those features' requirements. These requirements will not be
# automatically installed unless another package depends on them.
extras_requirements = {
    'reST': ['Sphinx>=1.6'],
}

setup(
    name=papas.__title__,
    version=papas.__version__,
    description=papas.__description__,
    long_description=long_description,
    keywords=papas.__keywords__,
    url=papas.__url__,
    download_url=papas.__url__,
    author=papas.__author__,
    author_email=papas.__author_email__,
    license=papas.__license__,
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
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    package_data={},
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    extras_require=extras_requirements,
    tests_require=tests_requirements,
    test_suite='tests',
)
