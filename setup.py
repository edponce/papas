#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


def loadfile(fn=''):
    '''
    Utility function to read a file and return its contents.
    Useful for loading documentation and long description files (e.g., README).
    '''
    return open(os.path.join(os.path.dirname(__file__), fn)).read()


requirements = [
]

setup_requirements = [
]

test_requirements = [
]

setup(
    name='PaPaS',
    version='1.0.0',
    author='Eduardo Ponce',
    author_email='eponcemo@utk.edu',
    description='A generic framework for parallel parameter studies.',
    long_description=loadfile('README.rst'),
    url='https://github.com/edponce/papas',
    license='MIT License',
    keywords='PaPaS',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platform='linux',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic : Utilities',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3',
    install_requires=requirements,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
)
