#!/usr/bin/python2

import sys
import os
import argparse
from argparse import RawTextHelpFormatter


# NOTE: The following are requirements to enable correct processing
#       * There is a data column named '[run number]'
#       * There is a data column named '[step]'
#       * Parameters varied are between '[run number]' and '[step]' columns
#       * Data records follow directly after column titles
#       * There is no empty record between data records and column titles
#       * All data values are numeric (integers or decimals)
#       * All data sections have the same number of columns and in same order
#       * Each data section has at least 2 header lines, one with less columns
#         than data columns


# Global variables
run_number_colstr = '[run number]'
step_colstr = '[step]'


def parseArgs():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(
        prog=__file__,
        description='NetLogo Output Parser:\n'
                    'Parse and order data from a combined/unordered '
                    'NetLogo output .csv file',
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--infile',
        type=str,
        dest='infile',
        default='',
        help='NetLogo .csv file with combined/unordered data'
    )

    parser.add_argument(
        '-o', '--outfile',
        type=str,
        dest='outfile',
        default='netlogo_ordered.csv',
        help='NetLogo .csv file with ordered data\n'
             'Default is \'netlogo_ordered.csv\''
    )

    args = parser.parse_args()

    # Validate options
    err = 0
    if not os.path.isfile(args.infile):
        print('ERROR: input file does not exist, ' + args.infile)
        err += 1

    if err != 0:
        print
        parser.print_help()
        sys.exit(os.EX_USAGE)

    return args


def processNetLogoCSV(infile='', outfile=''):
    '''
    Load, parse, and order data from NetLogo .csv file
    Write parsed data to output file
    '''
    infile = os.path.abspath(infile)

    print('NetLogo Output Parser is processing data...')
    print('  Input file:   ' + infile)
    print('  Output file:  ' + outfile)

    header_data = []
    raw_data = []

    first_header_flag = False  # enabled if the first header was read already

    # Assume all data records have same number of columns and in same order
    num_data_cols = 0  # number of data columns

    # Assume the file always begins with header lines
    header_or_data_flag = 0  # toggle flag: 0 = header, 1 = data

    run_number_col = 0  # identify column with 'run number' value
    run_number_lmax = 0  # local maximum 'run number', per data section
    run_number_gmax = 0  # global maximum 'run number'

    step_col = 0  # identify column with 'step' value

    # Process file line-by-line
    with open(infile) as f:
        for line in f:
            # Remove whitespace and quotes from input
            line = line.strip()
            line_split = [l.replace('"', '') for l in line.split(',')]
            ncols = len(line_split)

            # If first-time passing through header lines
            if not first_header_flag:
                header_data.append(tuple(line_split))  # save header

                # Assume .csv always have a column named 'run number'
                # before the data records
                if run_number_colstr in line:
                    first_header_flag = True
                    header_or_data_flag = 1
                    num_data_cols = ncols

                    # Get indices for 'run number' and 'step' columns
                    for i, x in enumerate(line_split):
                        if run_number_colstr in x:
                            run_number_col = i
                        elif step_colstr in x:
                            step_col = i

            else:
                # If number of columns do not match, assume it is the start
                # of another header
                if ncols != num_data_cols:
                    header_or_data_flag = 0

                # Assume .csv always have a column named 'run number'
                # before the data records
                elif run_number_colstr in line:
                    # increment global maximum 'run number'
                    run_number_gmax = run_number_gmax + run_number_lmax
                    run_number_lmax = 0  # reset local maximum 'run number'
                    header_or_data_flag = 1

                # Parse data records
                elif header_or_data_flag:
                    run_number = int(line_split[run_number_col])

                    if run_number > run_number_lmax:
                        run_number_lmax = run_number

                    line_split[run_number_col] = str(
                        run_number + run_number_gmax
                    )
                    raw_data.append(tuple([float(l) for l in line_split]))

    # Sort data based on parameters between 'run number' and 'step',
    # including 'step'
    sort_data = sorted(
        raw_data, key=lambda x: (x[run_number_col + 1:step_col + 1])
    )

    # Pretty print file stats
    print('  Header lines: ' + str(len(header_data)))
    print('  Data columns: ' + str(num_data_cols))
    print('  Data lines:   ' + str(len(sort_data)))

    # Write ordered data to output file
    with open(outfile, 'w') as f:
        # Write header data
        for line in header_data:
            f.write('%s\n' % ','.join(line))

        # Write data
        for line in sort_data:
            for i, x in enumerate(line):
                if i < (num_data_cols - 1):
                    f.write('%g,' % x)
                else:
                    f.write('%g\n' % x)


'''
Main entry point
'''
if __name__ == "__main__":
    args = parseArgs()
    processNetLogoCSV(args.infile, args.outfile)
