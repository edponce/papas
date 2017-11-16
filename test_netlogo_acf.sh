#!/bin/bash


DEBUG=1
PBS_O_WORKDIR=$(pwd)
SCRATCHDIR="$PBS_O_WORKDIR/workspace"

# Start timer
tic=$SECONDS

# Load Java module
module load java
cd $PBS_O_WORKDIR


#########################
#  User NetLogo Config  #
#########################
# NOTE: All files and directories must be in a network filesystem accessible from all hosts.

# Name of experiment run
experiment_name="Fire"

# Full path to input directory
input_dir="$PBS_O_WORKDIR/fire"

# Full path and filename of model file (.nlogo)
model_file="$input_dir/Fire.nlogo"

# Full path for all setup files (.xml)
setup_files_dir="$input_dir"

# Filename of setup files (.xml)
# NOTE: For large runs, use multiple files each with a subset of iterations or parameters.
#       Do not provide full paths, only the filenames.
setup_files=(Fire1.xml Fire2.xml Fire3.xml)

# Full path to working directory
# NOTE: Working directory is deleted after each run
work_dir="$SCRATCHDIR/fire"

# Full path to output directory
# NOTE: Gets created if it does not exists
output_dir="$input_dir/outputs"

# Filename of combined/unordered output file (.csv)
# NOTE: Do not provide full path, only the filename.
output_file="Fire.csv"

#------------------------------------------------------------------------------

# Full path and filename of NetLogo program (.jar)
netlogo_prog="$PBS_O_WORKDIR/NetLogo_6.0/app/netlogo-6.0.0.jar"

# Full path and filename of C++ MPI program
cpp_prog="$PBS_O_WORKDIR/netlogo_mpi"

# Full path and filename of Python parser program
parser_prog="$PBS_O_WORKDIR/netlogo_parser.py"


############################
#  Validate Configuration  #
############################
invalid_conf=0

# Validate input directory
if [ ! -d "$input_dir" ]; then
    echo "ERROR: input directory does not exists, $input_dir"
    invalid_conf=1
fi

# Validate model file
if [ ! -f "$model_file" ]; then
    echo "ERROR: model file does not exists, $model_file"
    invalid_conf=1
fi

# Validate setup files
for setup_file in "${setup_files[@]}"; do
    if [ ! -f "$setup_files_dir/$setup_file" ]; then
        echo "ERROR: setup file does not exists, $setup_files_dir/$setup_file"
        invalid_conf=1
    fi
done

# Validate working directory
if [ -d "$work_dir" ]; then
    rm -rf ${work_dir}/*
else
    mkdir -p $work_dir
fi

# Validate output directory
if [ ! -d "$output_dir" ]; then
    mkdir -p $output_dir
fi

# Validate NetLogo program
if [ ! -f "$netlogo_prog" ]; then
    echo "ERROR: NetLogo program does not exists, $netlogo_prog"
    invalid_conf=1
fi

# Validate C++ MPI program
if [ ! -f "$cpp_prog" ]; then
    echo "ERROR: C++ MPI program does not exists, $cpp_prog"
    invalid_conf=1
elif [ ! -x "$cpp_prog" ]; then
    echo "ERROR: C++ MPI program is not executable, $cpp_prog"
    invalid_conf=1
fi

# Validate Python parser program
if [ ! -f "$parser_prog" ]; then
    echo "ERROR: Python parser program does not exists, $parser_prog"
    invalid_conf=1
elif [ ! -x "$parser_prog" ]; then
    echo "ERROR: Python parser program is not executable, $parser_prog"
    invalid_conf=1
fi

# Exit if invalid configuration
if [ $invalid_conf -ne 0 ]; then
    exit
fi

echo
echo "NetLogo Configuration:"
echo "  Input directory: $input_dir"
echo "  Working directory: $work_dir"
echo "  Output directory: $output_dir"
echo "  Model file: $model_file"
echo "  Setup files: ${setup_files[@]}"
echo "  Output file: $output_file"


#########################
#  Launch NetLogo Runs  #
#########################
echo
echo "Launching Parallel NetLogo"

# Build command line for C++ MPI program, order of parameters matters (see netlogo_mpi.cpp)
cpp_prog_params="$netlogo_prog $experiment_name $model_file $work_dir/$output_file"
for setup_file in "${setup_files[@]}"; do
    cpp_prog_params+=" $setup_files_dir/$setup_file"
done

# Calculate number of processes per node
num_proc=${#setup_files[@]}

# Run parallel NetLogo
if [ $DEBUG -eq 1 ]; then
    echo "mpirun -np $num_proc $cpp_prog $cpp_prog_params"
else
    mpirun -np $num_proc $cpp_prog $cpp_prog_params
fi


#####################
#  Combine Outputs  #
#####################
echo
echo "Post-processing NetLogo Outputs ($output_dir)"

# Move to working directory
# NOTE: The following commands require we are in $work_dir, no full paths and filenames
cd $work_dir

# Check if output files were generated
if [ $(ls | wc -l) -gt 0 ]; then
    out_file="${output_file%.*}"
    out_ext="${output_file##*.}"

    # Append partial output files into single unordered output file
    if [ $DEBUG -eq 0 ]; then
        cat ${out_file}-*.${out_ext} >> $output_file
    fi

    # Parse and order output file
    if [ $DEBUG -eq 1 ]; then
        echo "$parser_prog -i $output_file -o ${out_file}_ordered.${out_ext}"
    else
        $parser_prog -i $output_file -o ${out_file}_ordered.${out_ext}
    fi

    # Transfer output data from working directory to output directory
    mv -f * $output_dir
else
    echo "WARN: no output files were generated"
fi

# Move to submission directory and clean working directory
cd $PBS_O_WORKDIR
rm -rf $work_dir


#################
#  Record Time  #
#################
# Stop timer
toc=$SECONDS
walltime=$((toc - tic))
hrs=$((walltime / 3600))
mins=$(((walltime % 3600) / 60))
secs=$(((walltime % 3600) % 60))
echo
echo "NetLogo job completed in $hrs h, $mins m, $secs s"
echo

