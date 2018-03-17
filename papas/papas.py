#!/usr/bin/env python3

'''
PaPaS: A lightweight and generic framework for parallel parameter studies

This program controls execution of workflows/programs for conducting
parameter studies in a parallel system.
A YAML or JSON configuration file is used to specify parameters with all their
possible values.
Parameters should be expected either from files, environment variables,
and/or command line arguments.

Example:
python3 papas.py -c papas_conf.json -a hello.json

Todo:
    * Create parser for custom regex expressions
    * Support workflow
    * Need function to substitute '%' from configuration files
    * Need function to split strings into list, but maintaining quoted strings
'''

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import subprocess
import json
import yaml
from configparse import MyParser


# default_papas_conf_file = 'papas_conf.json'
default_papas_conf_file = 'papas_conf.yml'
'''str: Default PaPaS JSON configuration file'''

args = None
'''obj: argparse.Namespace object with command line arguments'''


def print_log(msg='', *, end='\n', file=sys.stdout):
    '''
    Print output messages.

    Args:
        msg (str, optional): Information to print
            (default is empty string)
        end (char, optional): Character to print at end of message
            (default is newline)
        file (obj, optional): File descriptor for output
            (default is sys.stdout)
    '''
    print(msg, end=end, file=file)


def warn_log(msg='', *, end='\n', file=sys.stdout):
    '''
    Print warning messages.

    Args:
        msg (str, optional): Information to print
            (default is empty string)
        end (char, optional): Character to print at end of message
            (default is newline)
        file (obj, optional): File descriptor for output
            (default is sys.stdout)
    '''
    print('WARN: ' + msg, end=end, file=file)


def error_log(msg='', *, end='\n', file=sys.stderr):
    '''
    Print error messages.

    Args:
        msg (str, optional): Information to print
            (default is empty string)
        end (char, optional): Character to print at end of message
            (default is newline)
        file (obj, optional): File descriptor for output
            (default is sys.stderr)
    '''
    print('ERROR: ' + msg, end=end, file=file)


def debug_log(msg='', *, end='\n', file=sys.stdout):
    '''
    Print debugging messages.

    Args:
        msg (str, optional): Information to print
            (default is empty string)
        end (char, optional): Character to print at end of message
            (default is newline)
        file (obj, optional): File descriptor for output
            (default is sys.stderr)
    '''
    if args.conf_debug:
        print('DEBUG: ' + msg, end=end, file=file)


def parse_args():
    '''
    Parse and validate command line arguments.
    '''
    parser = argparse.ArgumentParser(
        prog=__file__,
        description='PaPaS: Framework for parallel parameter studies',
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        dest='conf_debug',
        help='Enable/disable debugging operations\n'
             'Default is disabled'
    )

    parser.add_argument(
        '-c', '--conf',
        type=str,
        dest='papas_conf_file',
        default=default_papas_conf_file,
        help='PaPaS YAML/JSON configuration file\n'
             'Default is \'' + default_papas_conf_file + '\''
    )

    parser.add_argument(
        '-a', '--app',
        type=str,
        dest='app_conf_file',
        default='',
        help='Application YAML/JSON configuration file'
    )

    global args
    args = parser.parse_args()

    # Validate options
    err = 0
    if not validate_file(args.papas_conf_file):
        err += 1

    if not validate_file(args.app_conf_file):
        err += 1

    if err:
        print_log()
        parser.print_help()
        sys.exit(os.EX_USAGE)


def validate_file(afile, *, dir=False, read=True, write=False, execute=False):
    '''
    Check access properties of a given file or directory, if it exists.
    Only checks for properties that are set to True, others are ignored.

    Args:
        afile (str): File or directory to check
        dir (bool, optional): Specify if it is a file or directory
            (default is False)
        read (bool, optional): Check if path is readable
            (default is True)
        write (bool, optional): Check if path is writeable
            (default is False)
        execute (bool, optional): Check if path is executable
            (default is False)

    Returns:
        bool: True if all properties set are supported, else False

    Todo:
        * Remove print messages, useful for debugging only
    '''
    prop_msg = []
    if not dir and not os.path.isfile(afile):
        prop_msg += ['file does not exists']
    elif dir and not os.path.isdir(afile):
        prop_msg += ['directory does not exists']
    else:
        if read and not os.access(afile, os.R_OK):
            prop_msg += ['is not readable']
        if write and not os.access(afile, os.W_OK):
            prop_msg += ['is not writable']
        if execute and not os.access(afile, os.X_OK):
            prop_msg += ['is not executable']

    if prop_msg:
        debug_log('\'%s\' %s' % (afile, ', '.join(prop_msg)))
        return False
    return True


def load_json_file(afile):
    '''
    Load a JSON configuration file.

    Args:
        afile (str): JSON file

    Returns:
        dict: Configuration data
    '''
    data = {}
    with open(afile, 'r') as f:
        data = json.load(f)
    return data


def load_yaml_file(afile):
    '''
    Load a YAML configuration file.

    Args:
        afile (str): YAML file

    Returns:
        dict: Configuration data
    '''
    data = {}
    with open(afile, 'r') as f:
        data = yaml.load(f)
    return data


def load_ini_file(afile):
    '''
    Load a INI configuration file.

    Args:
        afile (str): INI file

    Returns:
        dict: Configuration data
    '''
    return MyParser().load(afile)


def validate_papas_conf(conf_data):
    '''
    Parse and validate application configuration data.
    PaPaS mandatory keys are: extensions

    Args:
        conf_data (dict): Application configuration data
    '''
    pass


def validate_app_conf(conf_data):
    '''
    Validate application configuration data.

    Args:
        conf_data (dict): Application configuration data

    Returns:
        bool: True if configurations is valid, else False
    '''
    # Mandatory keys: program
    # Optional keys: params, dependences
    app_keys = ['program']
    for k in app_keys:
        if k not in conf_data:
            return False
    return True


def process_app_conf(papas_conf_data, app_conf_data):
    '''
    Parse and process application configuration data.

    Args:
        papas_conf_data (dict): PaPaS configuration data
        app_conf_data (dict): Application configuration data

    Todo:
        * Handle filenames with spaces
        * Parse command line tokens
    '''
    if not validate_app_conf(app_conf_data):
        error_log('invalid application JSON configuration.')
        return

    # Construct list of given command line
    '''
    Todo: Handle filenames with spaces
        * In JSON conf need to place filename between \'escaped quotes\'.
        * Before split, check for quotes and extract as a single token.
          Use [idx for idx, ltr in enumerate(prog_name) if ltr == '\'']
          to get all indices of quotes.
    '''
    prog_name = app_conf_data['program']
    cmd = prog_name.split()

    # Parse command line and identify executable program/file
    '''Todo: Parse command line tokens
        1. If single token:
            - If executable, then assume is an executable program as is.
              If no extension, assume is a command seen in PATH.
              If extension:
                  * If begins with slash append '.'
                  * If no slash append './'
            - If not executable, assume is a script identified by extension
        2. If multiple tokens:
            - If has environment variables, first token not an env variable
              apply the single token considerations
            - If no environment variables, use first token and
              apply the single token considerations
        3. In configuration dictionaries, can use '%' as a substitute for key.
    '''
    if len(cmd) == 1:
        if validate_file(cmd[0], execute=True):
            debug_log('File is executable')
        else:
            fn, fx = os.path.splitext(cmd[0])

            # Check if file extension is valid
            prog_tmp_str = papas_conf_data['file_extensions'].get(fx)
            if not prog_tmp_str:
                error_log('file not executable, no supported file extension')
                return

            if prog_tmp_str.find('%') >= 0:
                prog_str = prog_tmp_str.replace('%', fn)
                cmd = prog_str.split()
            else:
                cmd = prog_tmp_str.split() + cmd

    # Parse program parameters
    if 'params' in app_conf_data:
        for param, vals in app_conf_data['params'].items():
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
    # from timeit import Timer
    # t = Timer(
    #    'parse_args(); load_json_file(args.papas_conf_file)',
    #    'from __main__ import parse_args, load_json_file'
    # )
    # print_log(t.timeit(number=100))

    parse_args()
    # papas_conf_data = load_json_file(args.papas_conf_file)
    # app_conf_data = load_json_file(args.app_conf_file)
    papas_conf_data = load_yaml_file(args.papas_conf_file)
    app_conf_data = load_yaml_file(args.app_conf_file)
    # papas_conf_data = load_ini_file(args.papas_conf_file)
    # app_conf_data = load_ini_file(args.app_conf_file)

    validate_papas_conf(papas_conf_data)
    process_app_conf(papas_conf_data, app_conf_data)
