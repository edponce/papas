import os
from setuptools import setup


def read(fn=''):
    '''
    Utility function to read a long description file (e.g., README).
    '''
    return open(os.path.join(os.path.dirname(__file__), fn)).read()


setup(
    name = 'PaPaS',
    version = '1.0',
    author = 'Eduardo Ponce',
    author_email = 'eponcemo@utk.edu',
    description = (
        'A lightweight and generic framework for parallel parameter studies.'
    ),
    license = 'GPLv2',
    keywords = 'parallel parameter studies',
    url = 'https://github.com/edponce/papas',
    packages = [
        'PaPaS'
    ],
    long_description = read('README.md'),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Topic : Utilities',
        'License :: OSI Approved :: GPLv2'
    ]
)
