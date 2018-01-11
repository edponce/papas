#!/usr/bin/python3

import sys
import os
import argparse
from argparse import RawTextHelpFormatter


def parseArgs():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(prog=__file__, description='Test',
             formatter_class=RawTextHelpFormatter)

    parser.add_argument('-x', '--xparam', type=int, dest='x',
                        default=0,
                        help='An input parameter')

    args = parser.parse_args()

    # Validate options
    err = 0

    if err != 0:
        print()
        parser.print_help()
        sys.exit(os.EX_USAGE)

    return args


'''
Main entry point
'''
if __name__ == "__main__":
    args = parseArgs()
    if args.x > 1:
        print('Hello, world')
    else:
        print('Goodbye, world')

