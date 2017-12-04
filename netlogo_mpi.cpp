#include <iostream>
#include <sstream>
#include <cstdlib>
#include <string>
#include <mpi.h>

using namespace std;


int main(int argc, char* argv[])
{
    int numtasks = 1, rank = 0, len = 0, rc = 0;
    string hostname("localhost");

    // Initialize MPI library
    rc = MPI_Init(&argc, &argv);
    if (rc != MPI_SUCCESS) {
        cout << "ERROR: failed to initialize MPI environment" << endl << endl;
        MPI_Abort(MPI_COMM_WORLD, rc);
        return EXIT_FAILURE;
    }

    // Get number of MPI processes and unique rank IDs
    MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(&hostname[0], &len);

    // Get rank ID as a string
    ostringstream rank_str;
    rank_str << rank;

    /* Order of parameters:
     * 0 : program name (ignored)
     * 1 : java max heap memory
     * 2 : netlogo prog (full path and filename)
     * 3 : experiment name (single word)
     * 4 : model file (full path and filename)
     * 5 : out file (full path and filename)
     * 6 : setup files directory (without last slash)
     * 7-n : setup files (filename only)
     */
    // NOTE: Run 1 process per setup file
    // NOTE: Only processes that have a setup file will run NetLogo
    if ((argc > (numtasks + 7)) || (argc < 8)) {
        if (rank == 0) {
            cout << "Usage: " + string(argv[0]) + " [java_max_heap] [netlogo_prog] [experiment_name] [model_file] [output_file] [setup_files_directory] [setup_file1 setup_file2 ...]" << endl << endl;
            cout << "ERROR: incorrect number of parameters" << endl;
        }
    } else if (argc > (rank + 7)) {

        // Java max heap memory
        const string max_memory(argv[1]);

        // NetLogo program (.jar)
        const string netlogo_prog(argv[2]);

        // Experiment name
        string exp_name(argv[3]);
        exp_name = exp_name + "-" + rank_str.str();

        // Model file
        const string model_file(argv[4]);

        // Create partial output file based on rank ID
        string out_file(argv[5]);
        size_t ipos = out_file.find_last_of(".");
        out_file.insert(ipos, "-" + rank_str.str());

        // Setup files directory
        const string setup_files_dir(argv[6]);

        // Setup file
        const string setup_file(setup_files_dir + '/' + string(argv[rank + 7]));

        // Pretty print configuration
        cout << "  " + hostname + " (" + rank_str.str() + "):" +
		"\n    Java max memory:     " + max_memory +
		"\n    NetLogo program:     " + netlogo_prog +
	    "\n    Experiment name:     " + exp_name +
		"\n    Model file:          " + model_file +
		"\n    Setup file:          " + setup_file +
		"\n    Partial output file: " + out_file + "\n\n";

        const string cmd("java -Xmx" + max_memory + " -Dfile.encoding=UTF-8 -cp " + netlogo_prog + " org.nlogo.headless.Main --experiment " + exp_name + " --model " + model_file + " --setup-file " + setup_file + " --table " + out_file);

        //cout << cmd << endl << endl;
        system(cmd.c_str());
    } else {
        cout << "  " + hostname + " (" + rank_str.str() + "): no setup file assigned\n\n";
    }

    MPI_Finalize();

    return EXIT_SUCCESS;
}

