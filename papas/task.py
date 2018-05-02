#!/usr/bin/env python3


__all__ = ['Task']


import utils.logger


class Task(object):

    def __init__(self, **conf):
        self.logger = utils.logger.init_logger('task')
        self.task_id = -1
        self.task_conf = {}

        if 'task_id' in conf:
            self.task_id = conf['task_id']
        if 'conf' in conf:
            self.task_conf = conf['conf']

    def print(self):
        if self.task_conf:
            print(self.task_conf)
        else:
            self.logger.debug('No task configuration data to print')

    def __str__(self):
        self.print()
