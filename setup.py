import os
from setuptools import setup


def read(fn=''):
    '''
    Utility function to read a long description file (e.g., README).
    '''
    return open(os.path.join(os.path.dirname(__file__), fn)).read()


requirements = [
]

setup_requirements = [
]

test_requirements = [
]

setup(
    name = 'PaPaS',
    version = '1.0',
    author = 'Eduardo Ponce',
    author_email = 'eponcemo@utk.edu',
    description = 'A lightweight and generic framework for parallel parameter studies.',
    long_description = read('README.rst'),
    url = 'https://github.com/edponce/papas',
    install_requires=requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    license = 'GPLv2',
    keywords = 'parallel parameter studies',
    packages = [
        'PaPaS'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Topic : Utilities',
        'License :: OSI Approved :: GPLv2',
        'Programming Language :: Python :: 3'
    ]
)
