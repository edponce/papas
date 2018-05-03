#!/usr/bin/env python3


"""PaPaS: A lightweight and generic framework for parallel parameter studies

This program controls execution of workflows/programs for conducting
parameter studies in a parallel system.
A YAML/JSON/INI configuration file is used to specify parameters with all their
possible values.
Parameters should be expected either from files, environment variables,
and/or command line arguments.


Example
=======

python3 papas.py -a tasks_conf/YAML_conf/helloWorld.yml
"""


# import sys
import os
import argparse
from papas import PaPaS


default_conf_file = 'papas_conf/PaPaS.yml'
"""str: Default PaPaS configuration file"""


def parse_args():
    """Parse and validate command line arguments

    Returns:
        argparse.Namespace: object with command line argument name/values
    """

    parser = argparse.ArgumentParser(
        prog=__file__,
        description='PaPaS: Framework for parallel parameter studies',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-c', '--conf', type=str, dest='conf',
        default=default_conf_file,
        help='PaPaS YAML/JSON/INI configuration file\n'
             'Default is \'' + default_conf_file + '\''
    )

    parser.add_argument(
        '-a', '--app', type=str, dest='app_conf',
        default='',
        help='Application YAML/JSON/INI configuration file'
    )

    return parser.parse_args()


def process_app_conf(conf_data, app_conf_data):
    """Parse and process application configuration data

    Args:
        conf_data (dict): PaPaS configuration data
        app_conf_data (dict): Application configuration data

    Todo:
        * Handle filenames with spaces
        * Parse command line tokens
    """
    if not validate_app_conf(app_conf_data):
        print('invalid application configuration.')
        return

    # Construct list of given command line
    """ Todo: Handle filenames with spaces
        * In JSON conf need to place filename between \'escaped quotes\'.
        * Before split, check for quotes and extract as a single token.
          Use [idx for idx, ltr in enumerate(prog_name) if ltr == '\'']
          to get all indices of quotes.
    """
    prog_name = app_conf_data['command']
    cmd = prog_name.split()

    # Parse command line and identify executable program/file
    """Todo: Parse command line tokens
        * If single token:
            - If executable, then assume is an executable program as is.
              If no extension, assume is a command seen in PATH.
              If extension:
                  * If begins with slash append '.'
                  * If no slash append './'
            - If not executable, assume is a script identified by extension
        * If multiple tokens:
            - If has environment variables, first token not an env variable
              apply the single token considerations
            - If no environment variables, use first token and
              apply the single token considerations
        * In configuration dictionaries, can use '%' as a substitute for key.
    """
    if len(cmd) == 1:
        if validate_file(cmd[0], execute=True):
            print('File is executable')
        else:
            fn, fx = os.path.splitext(cmd[0])

            # Check if file extension is valid
            prog_tmp_str = conf_data['file_extensions'].get(fx[1:])
            if not prog_tmp_str:
                print('file not executable, no supported file extension')
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


if __name__ == '__main__':
    args = parse_args()
    pp = PaPaS(**vars(args))
    print(pp)
    pp.print_app()
