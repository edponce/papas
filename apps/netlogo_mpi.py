#!/usr/bin/env python2

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
from mpi4py import MPI  # MPI.Init() is called when mpi4py is imported
                        # MPI.Finalize() is called automatically at end of script


def parseArgs():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(prog=__file__,
             description='NetLogo MPI: process dispatcher using MPI',
             formatter_class=RawTextHelpFormatter)

    parser.add_argument('-p', '--maxheap', type=str, dest='max_memory',
                        default='16g',
                        help='Java maximum heap memory per process')

    parser.add_argument('-n', '--netlogo', type=str, dest='netlogo_prog',
                        default='',
                        help='NetLogo Java program (full path)')

    parser.add_argument('-e', '--experiment', type=str, dest='exp_name',
                        default='Experiment',
                        help='Experiment name (no whitespaces)')

    parser.add_argument('-m', '--modelfile', type=str, dest='model_file',
                        default='',
                        help='Model file (full path)')

    parser.add_argument('-o', '--outfile', type=str, dest='out_file',
                        default='Experiment.csv',
                        help='Output file (full path)')

    parser.add_argument('-d', '--setupdirectory', type=str, dest='setup_files_dir',
                        default='',
                        help='Directory of setup files')

    parser.add_argument('-s', '--setupfiles', type=str, dest='setup_files',
                        default='', nargs='+', metavar=('S1', 'S2'),
                        help='Setup files (without last slash)')

    args = parser.parse_args()

    # Validate options
    err = 0
    if args.max_memory not in ['1g','2g','4g','8g','16g','32g']:
        print 'ERROR: invalid max heap size, ' + args.max_memory
        err += 1

    if not os.path.isfile(args.netlogo_prog):
        print 'ERROR: NetLogo program does not exists, ' + args.netlogo_prog
        err += 1

    if not os.path.isfile(args.model_file):
        print 'ERROR: NetLogo model file does not exists, ' + args.model_file
        err += 1

    setup_files_dir_flag = 0
    if args.setup_files_dir:
        if not os.path.isdir(args.setup_files_dir):
            print 'ERROR: NetLogo setup files directory does not exists, ' + args.setup_files_dir
            err += 1
        else:
            setup_files_dir_flag = 1

    if len(args.setup_files) > 0:
        for setup_file in args.setup_files:
            if setup_files_dir_flag:
                setup_file = args.setup_files_dir + '/' + setup_file
            if not os.path.isfile(setup_file):
                print 'ERROR: NetLogo setup file does not exists, ' + setup_file
                err += 1
    else:
        print 'ERROR: no NetLogo setup files provided'
        err += 1

    if err != 0:
        print
        parser.print_help()
        sys.exit(os.EX_USAGE)

    return args


'''
Main entry point
'''
if __name__ == "__main__":
    # Parse command line arguments
    args = parseArgs()

    # Get number of MPI processes and unique rank IDs
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    hostname = MPI.Get_processor_name()

    # NOTE: Only processes that have a setup file will run NetLogo
    if rank < len(args.setup_files):
        print '  ' + hostname + ' (' + str(rank) + '):' + \
              '\n    Java max memory:     ' + args.max_memory + \
              '\n    NetLogo program:     ' + args.netlogo_prog + \
              '\n    Experiment name:     ' + args.exp_name + \
              '\n    Model file:          ' + args.model_file + \
              '\n    Setup file:          ' + args.setup_files[rank] + \
              '\n    Partial output file: ' + args.out_file + '\n'
    else:
        print '  ' + hostname + ' (' + str(rank) + '): no setup file assigned\n'

    comm.Barrier()

