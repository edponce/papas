#!/usr/bin/env python3


import argparse


def parseArgs():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        prog=__file__,
        description='Hello World test program',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-x', '--xparam', type=int,
        dest='x',
        default=0,
        help='An input parameter'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    if args.x > 10:
        print('Hello, world!')
    else:
        print('Goodbye, world!')
