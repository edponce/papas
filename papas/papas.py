#!/usr/bin/env python3


__all__ = ['PaPaS']


import os
# import sys
# import subprocess
import json
import yaml
from utils.logger import logger


class PaPaS(object):

    _logger = logger

    def __init__(self, **kwargs):
        self.papas_data = {}
        self.app_data = {}

        if 'conf' in kwargs:
            self.load_papas(kwargs['conf'])
        if 'app' in kwargs:
            self.load_app(kwargs['app'])

    def load_conf(self, conf=''):
        """Load PaPaS configuration

        Args:
            conf (file|str|dict): YAML, JSON, or INI file

        Returns:
            dict: Configuration data
        """
        data = {}
        # It is a dict
        if isinstance(conf, dict):
            type(self)._logger.debug('Loading PaPaS configuration from existing '
                              'dictionary')
            data = conf
        # It is a list
        elif isinstance(conf, list):
            type(self)._logger.debug('Loading PaPaS configuration from existing '
                              'list')
            data = conf
        elif isinstance(conf, str):
            # It is an existing file
            if os.path.isfile(conf):
                fn, xt = os.path.splitext(conf)
                ext = xt[1:].lower()
                if ext in ['yaml', 'yml']:
                    type(self)._logger.debug('Loading PaPaS configuration from '
                                      'YAML file')
                    with open(conf, 'r') as fd:
                        data = yaml.load(fd)
                elif ext in ['json']:
                    type(self)._logger.debug('Loading PaPaS configuration from '
                                      'JSON file')
                    with open(conf, 'r') as fd:
                        data = json.load(fd)
                elif ext in ['ini']:
                    type(self)._logger.debug('Loading PaPaS configuration from '
                                      'INI file')
                    # with open(conf, 'r') as fd:
                    #    data = ini.load(fd)
            # Check YAML/JSON/INI string
            else:
                try:
                    data = yaml.load(conf)
                except yaml.YAMLError as exc:
                    if hasattr(exc, 'problem_mark'):
                        mark = exc.problem_mark
                        type(self)._logger.info('Error loading configuration data'
                                         ' as YAML format (%s:%s): %s' %
                              (mark.line + 1, mark.column + 1, exc))
                    else:
                        type(self)._logger.info('Error loading configuration data'
                                         ' as YAML format: ', exc)
                    pass
                else:
                    type(self)._logger.debug('Loading PaPaS configuration from '
                                      'YAML string')
                try:
                    data = json.load(conf)
                except json.JSONDecodeError as exc:
                    type(self)._logger.info('Error loading configuration data'
                                     ' as JSON format: ', exc)
                    pass
                else:
                    type(self)._logger.debug('Loading PaPaS configuration from '
                                      'JSON string')
                # try:
                #    data = ini.load(conf)
                # except:
                #    pass
                # else:
                #    type(self)._logger.debug('Loading PaPaS configuration from '
                #                      'INI string')

        return data

    def load_papas(self, conf=''):
        """Load PaPaS configuration
        Data is validated and organized

        Args:
            conf (file|str|dict): YAML, JSON, or INI file

        Returns:
        """
        data = self.load_conf(conf)
        if self.validate_papas(data):
            self.papas_data = data

    def dump_papas(self):
        if self.papas_data:
            pass

    def __repr__(self):
        s = str(self.papas_data)
        for k, v in self.app_data.items():
            s += '\n\n' + k + ': ' + str(v)
        return s

    def validate_papas(self, data):
        """Validate and clean configuration data"""
        return True

    def load_app(self, conf=''):
        """Load application configuration
        Data is validated and organized

        Args:
            conf (file|str|dict): YAML, JSON, or INI file

        Returns:
        """
        data = self.load_conf(conf)
        if self.validate_app(data):
            self.app_data = data

    def dump_app(self):
        pass

    def validate_app(self, data):
        """Validate application configuration data

        Args:
            data (dict): Application configuration data

        Returns:
            bool: True if configurations is valid, else False
        """
        app_keys = ['command']
        if isinstance(data, dict):
            for d in data.keys():
                for k in app_keys:
                    if k not in data[d].keys():
                        return False
        elif isinstance(data, list):
            for l in data:
                for k in app_keys:
                    if k not in l.keys():
                        return False
        return True

    def interpolate(self):
        pass

    def resolve_dependencies(self):
        pass

    def run(self):
        pass

    def detect_system(self):
        pass

    def build_batch_script(self):
        pass

    def build_ssh_script(self):
        pass

    def clear(self):
        self.app_data = {}
