#!/bin/bash


# This is a testing submission script used to validate NetLogo configuration and setup.
# For this script to work correctly, the following requirements should be satisfied:
#   * This script should be executed from 'mpi_netlogo' directory
#   * NetLogo_6.0 (real or symlink) should be available in 'mpi_netlogo'


# 0 - run in localhost
# 1 - simulate run
DEBUG=1


# Imitate ACF cluster environment
PBS_O_WORKDIR="$(pwd)"
SCRATCHDIR="$PBS_O_WORKDIR"

# Move to submission directory
cd "$PBS_O_WORKDIR"


#########################
#  User NetLogo Config  #
#########################
# Name of experiment run
experiment_name="Fire"

# Full path to top directory of project
top_dir="$PBS_O_WORKDIR"

# Full path and filename of model file (.nlogo)
model_file="$top_dir/Fire.nlogo"

# Full path for all setup files (.xml)
setup_files_dir="$top_dir"

# Filename of setup files (.xml)
# NOTE: Do not provide full paths, only the filenames.
# 1. For runs with many parameters, use different files,
#    each with a subset of parameters.
#setup_files=(
#Fire1.xml
#Fire2.xml
#Fire3.xml
#)
# 2. For runs with same parameters but many iterations,
#    use multiple times a single file with a subset of iterations.
setup_files=(
Fire.xml
Fire.xml
)

# Full path to working directory
# NOTE: Working directory is created/removed after each run
# NOTE: If running simultaneous jobs, each must have a unique working directory
work_dir="$SCRATCHDIR/${experiment_name}_workspace"

# Full path to output directory
# NOTE: Gets created if it does not exists
output_dir="$top_dir/outputs2"

# Filename of combined/unordered output file (.csv)
# NOTE: Do not provide full path, only the filename.
output_file="Fire.csv"

#------------------------------------------------------------------------------

# Java max heap memory allowed (k = KB, m = MB, g = GB)
java_max_memory="32g"

# Full path to directory of MPI NetLogo project
# Available at: https://github.com/edponce/mpi_netlogo
mpi_netlogo_dir="$HOME/netlogo/mpi_netlogo"

# Full path and filename of NetLogo program (.jar)
netlogo_prog="$mpi_netlogo_dir/NetLogo_6.0/app/netlogo-6.0.0.jar"

# Full path and filename of C++ MPI program
cpp_prog="$mpi_netlogo_dir/netlogo_mpi"

# Full path and filename of Python parser program
parser_prog="$mpi_netlogo_dir/netlogo_output_parser.py"


#################
#  Record Time  #
#################
# Start timer
tic=$SECONDS


############################
#  Validate Configuration  #
############################
invalid_conf=0

# Validate top directory
if [ ! -d "$top_dir" ]; then
    echo "ERROR: top directory does not exists, $top_dir"
    invalid_conf=1
fi

# Validate model file
if [ ! -f "$model_file" ]; then
    echo "ERROR: model file does not exists, $model_file"
    invalid_conf=1
fi

# Validate setup files
if [ ${#setup_files[@]} -lt 1 ]; then
    echo "ERROR: no setup file was provided"
    invalid_conf=1
else
    for setup_file in "${setup_files[@]}"; do
        if [ ! -f "$setup_files_dir/$setup_file" ]; then
            echo "ERROR: setup file does not exists, $setup_files_dir/$setup_file"
            invalid_conf=1
        fi
    done
fi

# Validate working directory
if [ $DEBUG -eq 0 ]; then
    if [ -d "$work_dir" ]; then
        rm -rf "$work_dir"/*
    else
        mkdir -p "$work_dir"
    fi
fi

# Validate output directory
if [ $DEBUG -eq 0 ]; then
    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi
fi

# Validate MPI NetLogo directory
if [ ! -d "$mpi_netlogo_dir" ]; then
    echo "ERROR: MPI NetLogo directory does not exists, $mpi_netlogo_dir"
    invalid_conf=1
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

# Cleanup and exit if invalid configuration
if [ $invalid_conf -ne 0 ]; then
    rm -rf "$work_dir" "$output_dir"
    exit
fi

echo
echo "NetLogo Configuration:"
echo "  Java max memory:       $java_max_memory"
echo "  NetLogo program:       $netlogo_prog"
echo "  Experiment name:       $experiment_name"
echo "  Model file:            $model_file"
echo "  Setup files directory: $setup_files_dir"
echo "  Setup files:           ${setup_files[@]}"
echo "  Working directory:     $work_dir"
echo "  Combined output file:  $output_file"
echo "  Output directory:      $output_dir"


#########################
#  Launch NetLogo Runs  #
#########################

# Load Java module
if [ "$(command -v module)" ]; then
    module load java
fi

# Calculate number of MPI processes
num_proc=${#setup_files[@]}

# Build command line for C++ MPI program, order of parameters matters (see netlogo_mpi.cpp)
cpp_prog_params="$java_max_memory $netlogo_prog $experiment_name $model_file $work_dir/$output_file $setup_files_dir ${setup_files[@]}"

echo
echo "Launching $num_proc Parallel NetLogo Jobs"

# Run parallel NetLogo
if [ $DEBUG -eq 1 ]; then
    echo "mpirun -np $num_proc $cpp_prog $cpp_prog_params"
else
    mpirun -np $num_proc "$cpp_prog" $cpp_prog_params
fi


#####################
#  Combine Outputs  #
#####################
echo
echo "Post-processing NetLogo Outputs"

# Check if output files were generated
if [ $(ls | wc -l) -gt 0 ]; then
    out_file="${output_file%.*}"
    out_ext="${output_file##*.}"
    output_ordered_file="${out_file}_ordered.$out_ext"

    if [ $DEBUG -eq 1 ]; then
        echo "$parser_prog -i $work_dir/$output_file -o $work_dir/$output_ordered_file"
    else
        # Combine partial output files into a single unordered output file
        cat $work_dir/$out_file-*.$out_ext >> "$work_dir/$output_file"

        # Parse unordered output file and generate combined ordered output file
        $parser_prog -i "$work_dir/$output_file" -o "$work_dir/$output_ordered_file"

        echo
        echo "Transferring data from working to output directory"
        echo "  Working directory:    $work_dir"
        echo "  Combined output file: $output_file"
        echo "  Output ordered file:  $output_ordered_file"
        echo "  Output directory:     $output_dir"

        # Transfer output data from working directory to output directory
        mv -f "$work_dir/$output_file" "$work_dir/$output_ordered_file" "$output_dir"
    fi
else
    echo "ERROR: no output files were generated"
fi

# Remove working directory
rm -rf "$work_dir"


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
echo "Job completed in $hrs h, $mins m, $secs s"
echo

