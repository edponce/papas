#!/usr/bin/env python3

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import subprocess
import json


def parseArgs():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(prog=__file__,
             description='JSON Parser: parse JSON configuration file',
             formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c', '--conf', type=str, dest='papas_conf_file',
                        default='papas_conf.json',
                        help='PaPaS JSON configuration file\n'
                             'Default is papas_conf.json')

    parser.add_argument('-a', '--app', type=str, dest='app_conf_file',
                        default='',
                        help='Application JSON configuration file')

    args = parser.parse_args()

    # Validate options
    err = 0
    if not os.path.isfile(args.app_conf_file):
        print('ERROR: Application JSON configuration file does not exist, ' + args.app_conf_file)
        err += 1

    if not os.path.isfile(args.papas_conf_file):
        print('ERROR: PaPaS JSON configuration file does not exist, ' + args.papas_conf_file)
        err += 1

    if err != 0:
        print()
        parser.print_help()
        sys.exit(os.EX_USAGE)

    return args


def loadConfData(conf_file=''):
    '''
    Load a JSON configuration file
    '''
    conf_data = {}
    with open(os.path.abspath(conf_file), 'r') as f:
        conf_data = json.load(f)

    return conf_data


def processAppConf(papas_conf_data={}, app_conf_data={}):
    '''
    Parse configuration data
    Application mandatory keys are: program#, params#, and dependences
    PaPaS mandatory keys are: extensions
    '''

    # Construct command line
    cmd = []

    # Check for env variables pre-application.
    # Check for extensions to auto-detect C/C++/Python/Java/etc.
    # Append ./ only if single word and it is an executable
    prog_name = app_conf_data['program1']
    if os.access(prog_name, os.X_OK):
        cmd.append('./' + prog_name)
    else:
        cmd.append(prog_name)

    for param, vals in app_conf_data['params1'].items():
        if isinstance(vals, list) and len(vals) > 1:
            for val in vals:
                cmd.append(param)
                cmd.append(val)
        else:
            cmd.append(param)
            cmd.append(vals)

    print(' '.join(cmd))
    subprocess.run(cmd)


'''
Main entry point
'''
if __name__ == "__main__":
    args = parseArgs()
    papas_conf_data = loadConfData(args.papas_conf_file)
    app_conf_data = loadConfData(args.app_conf_file)
    processAppConf(papas_conf_data, app_conf_data)

