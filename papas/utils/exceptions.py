#!/usr/bin/env python3


class Error(Exception):
    '''Base class for exceptions'''

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message


class InterpolationError(Error):
    '''Base class for interpolation-related exceptions'''

    def __init__(self, name, value, msg):
        Error.__init__(self, msg)
        self.value = value
        self.name = name
