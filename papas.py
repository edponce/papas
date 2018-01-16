#!/usr/bin/env python3

'''
PaPaS: A lightweight and generic framework for parallel parameter studies

This program controls execution of workflows/programs for conducting
parameter studies in a parallel system.
A JSON configuration file is used to specify parameters with all their
possible values.

Example:
python3 papas.py -c papas_conf.json -a hello.json

Todo:
    * Create parser for custom regex expressions
    * Support workflow
'''

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import subprocess
import json


default_papas_conf_file = 'papas_conf.json'
'''str: Default PaPaS JSON configuration file.'''


def print_log(msg='', *, end='\n', file=sys.stdout):
    '''
    Print messages.

    Kwargs:
        msg (str): Information to print

    Kwoargs:
        |  end (char): Character to print at end of message
        |  file (obj): file descriptor for output
    '''
    print(msg, end=end, file=file)


def warn_log(msg='', *, end='\n', file=sys.stdout):
    '''
    Print messages.

    Kwargs:
        msg (str): Information to print

    Kwoargs:
        end (char): Character to print at end of message
        file (obj): file descriptor for output
    '''
    print('WARN: ' + msg, end=end, file=file)


def error_log(msg='', *, end='\n', file=sys.stderr):
    '''
    Print messages.

    Kwargs:
        msg (str): Information to print

    Kwoargs:
        end (char): Character to print at end of message
        file (obj): file descriptor for output
    '''
    print('ERROR: ' + msg, end=end, file=file)


def parse_args():
    '''
    Parse and validate command line arguments.

    Returns:
        object: An argparse.Namespace object
    '''
    parser = argparse.ArgumentParser(prog=__file__,
             description='PaPaS: Framework for parallel parameter studies',
             formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c', '--conf', type=str, dest='papas_conf_file',
                        default=default_papas_conf_file,
                        help='PaPaS JSON configuration file\n'
                             'Default is \'' + default_papas_conf_file + '\'')

    parser.add_argument('-a', '--app', type=str, dest='app_conf_file',
                        default='',
                        help='Application JSON configuration file')

    args = parser.parse_args()

    # Validate options
    err = 0
    if not validate_path(args.papas_conf_file, read=True):
        err += 1

    if not validate_path(args.app_conf_file, read=True):
        err += 1

    if err:
        print_log()
        parser.print_help()
        sys.exit(os.EX_USAGE)

    return args


def validate_path(apath, *, file=True, read=False, write=False, execute=False):
    '''
    Check access properties of a given file or directory, if it exists.
    Returns True or False.

    Positional arguments:
        apath -- file or directory to check

    Keyword-only arguments:
        file -- specify if it is a file or directory (default is True)
        read -- check if path is readable (default is False)
        write -- check if path is writeable (default is False)
        execute -- check if path is executable (default is False)
    '''
    prop_msg = []
    if file and not os.path.isfile(apath):
        prop_msg += ['file does not exists']
    elif not file and not os.path.isdir(apath):
        prop_msg += ['directory does not exists']
    else:
        if read and not os.access(apath, os.R_OK):
            prop_msg += ['is not readable']
        if write and not os.access(apath, os.W_OK):
            prop_msg += ['is not writable']
        if execute and not os.access(apath, os.X_OK):
            prop_msg += ['is not executable']

    if prop_msg:
        error_log('\'%s\' %s' % (apath, ', '.join(prop_msg)))
        return False
    return True


def load_json_file(afile):
    '''
    Load a JSON configuration file.
    Returns data in a dictionary.

    Positional arguments:
        apath -- JSON file
    '''
    data = {}
    with open(afile, 'r') as f:
        data = json.load(f)
    return data


def process_papas_conf(conf_data):
    '''
    Parse and validate application configuration data.
    PaPaS mandatory keys are: extensions

    Positional arguments:
        conf_data -- application configuration data
    '''
    pass


def validate_app_conf(conf_data):
    '''
    Validate application configuration data.
    Returns True or False.

    Positional arguments:
        conf_data -- application configuration data
    '''
    # Check mandatory keys: program, params, and dependences
    app_keys = ['program', 'params']
    for k in app_keys:
        if k not in conf_data:
            return False
    return True


def process_app_conf(conf_data):
    '''
    Parse and process application configuration data.

    Positional arguments:
        conf_data -- application configuration data
    '''
    if not validate_app_conf(conf_data):
        error_log('invalid application JSON configuration.')
        return

    # Construct command line
    cmd = []

    # Check for env variables pre-application.
    # Check for extensions to auto-detect C/C++/Python/Java/etc.
    # Append ./ only if single word and it is an executable
    prog_name = conf_data['program']
    if ' ' in prog_name:
        for i in prog_name.split():
            cmd.append(i)
    else:
        if validate_path(prog_name, execute=True):
            prestr = ''
            '''
            if '/' == prog_name[0]:
                prestr = '.'
            elif './' != prog_name[:2]:
                prestr = './'
            '''
            cmd.append(prestr + prog_name)

    for param, vals in conf_data['params'].items():
        if isinstance(vals, list) and len(vals) > 1:
            for val in vals:
                cmd.append(param)
                cmd.append(val)
        else:
            cmd.append(param)
            cmd.append(vals)

    print(cmd)
    subprocess.run(cmd)


'''
Main entry point
'''
if __name__ == '__main__':
    #from timeit import Timer
    #t = Timer('args = parse_args(); load_json_file(args.papas_conf_file)', 'from __main__ import parse_args, load_json_file')
    #print_log(t.timeit(number=100))

    args = parse_args()
    papas_conf_data = load_json_file(args.papas_conf_file)
    app_conf_data = load_json_file(args.app_conf_file)
    process_papas_conf(papas_conf_data)
    process_app_conf(app_conf_data)

