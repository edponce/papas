#!/usr/bin/env python3


__all__ = ['Task', 'PTask']


from utils.logger import logger


class Task(object):
    """Task instance with a specific set of resolved parameters"""

    _tid = 0
    _logger = logger

    def __init__(self, **kwargs):
        self.conf = {}

        if 'conf' in kwargs:
            self.conf = kwargs['conf']

    def __repr__(self):
        return str(self.conf)


class PTask(object):
    """Task instance with unresolved parameters representing a list of Tasks"""

    _tid = 0
    _logger = logger

    def __init__(self, **kwargs):
        self.conf = {}
        self.tasks = []

        if 'conf' in kwargs:
            self.conf = kwargs['conf']

    def print_tasks(self):
        for t in self.tasks:
            print(t)

    def __repr__(self):
        return str(self.conf)
