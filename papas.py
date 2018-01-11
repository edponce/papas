#!/usr/bin/python3

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

    parser.add_argument('-j', '--jsonfile', type=str, dest='jsonfile',
                        default='',
                        help='JSON configuration file')

    args = parser.parse_args()

    # Validate options
    err = 0
    if not os.path.isfile(args.jsonfile):
        print('ERROR: JSON configuration file does not exist, ' + args.jsonfile)
        err += 1

    if err != 0:
        print()
        parser.print_help()
        sys.exit(os.EX_USAGE)

    return args


def processJSONfile(jsonfile=''):
    '''
    Load and parse JSON configuration file
    '''
    jsonfile = os.path.abspath(jsonfile)

    # Load JSON data
    # Mandatory keywords are: program#, params#, and dependences
    with open(jsonfile, 'r') as f:
        config = json.load(f)

    # Construct command line
    cmd = []

    # Check for extensions to auto-detect C/C++/Python/Java/etc.
    # Append ./ only if single word and it is an executable
    prog_name = config['program1']
    if os.access(prog_name, os.X_OK):
        cmd.append('./' + prog_name)
    else:
        cmd.append(prog_name)

    for param, vals in config['params1'].items():
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
    processJSONfile(args.jsonfile)

