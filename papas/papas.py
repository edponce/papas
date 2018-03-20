#!/usr/bin/env python3


__all__ = ['PaPaSDriver']


import os
# import sys
# import subprocess
import json
import yaml
import logging


def init_logger():
    """Configure logging"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    log_file_handler = logging.FileHandler(__name__ + '.log')
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)
    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setLevel(logging.INFO)
    log_stream_handler.setFormatter(formatter)
    logger.addHandler(log_stream_handler)

    return logger


class PaPaSDriver:

    def __init__(self, **conf):
        self.logger = init_logger()
        self.papas_data = {}
        self.app_data = {}

        if 'conf' in conf:
            self.load_papas(conf['conf'])
        if 'app' in conf:
            self.load_app(conf['app'])

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
            self.logger.debug('Loading PaPaS configuration from existing '
                              'dictionary')
            data = conf
        # It is a list
        elif isinstance(conf, list):
            self.logger.debug('Loading PaPaS configuration from existing '
                              'list')
            data = conf
        elif isinstance(conf, str):
            # It is an existing file
            if os.path.isfile(conf):
                fn, xt = os.path.splitext(conf)
                ext = xt[1:].lower()
                if ext in ('yaml', 'yml'):
                    self.logger.debug('Loading PaPaS configuration from '
                                      'YAML file')
                    with open(conf, 'r') as fd:
                        data = yaml.load(fd)
                elif ext in ('json'):
                    self.logger.debug('Loading PaPaS configuration from '
                                      'JSON file')
                    with open(conf, 'r') as fd:
                        data = json.load(fd)
                elif ext in ('ini'):
                    self.logger.debug('Loading PaPaS configuration from '
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
                        self.logger.info('Error loading configuration data'
                                         ' as YAML format (%s:%s): %s' %
                              (mark.line + 1, mark.column + 1, exc))
                    else:
                        self.logger.info('Error loading configuration data'
                                         ' as YAML format: ', exc)
                    pass
                else:
                    self.logger.debug('Loading PaPaS configuration from '
                                      'YAML string')
                try:
                    data = json.load(conf)
                except json.JSONDecodeError as exc:
                    self.logger.info('Error loading configuration data'
                                     ' as JSON format: ', exc)
                    pass
                else:
                    self.logger.debug('Loading PaPaS configuration from '
                                      'JSON string')
                # try:
                #    data = ini.load(conf)
                # except:
                #    pass
                # else:
                #    self.logger.debug('Loading PaPaS configuration from '
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
        self.papas_data = self.validate_papas(data)

    def dump_papas(self):
        if self.papas_data:
            pass

    def print_papas(self):
        if self.papas_data:
            print(self.papas_data)
        else:
            self.logger.debug('No PaPaS configuration data to print')

    def validate_papas(self, data):
        """Validate and clean configuration data"""
        return data

    def load_app(self, conf=''):
        """Load application configuration
        Data is validated and organized

        Args:
            conf (file|str|dict): YAML, JSON, or INI file

        Returns:
        """
        data = self.load_conf(conf)
        self.app_data = self.validate_app(data)

    def dump_app(self):
        pass

    def print_app(self):
        if self.app_data:
            print(self.app_data)
        else:
            self.logger.debug('No application configuration data to print')

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
