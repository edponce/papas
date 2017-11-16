#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <string>
#include <mpi.h>

using namespace std;


int main(int argc, char* argv[])
{
    int numtasks = 1, rank = 0, len = 0, rc = 0;
    char hostname[MPI_MAX_PROCESSOR_NAME] = { "localhost" };

    // Initialize MPI library
    rc = MPI_Init(&argc, &argv);
    if (rc != MPI_SUCCESS) {
        cout << "Error starting MPI program. Terminating." << endl;
        MPI_Abort(MPI_COMM_WORLD, rc);
        return 0;
    }

    // Get number of MPI processes and unique rank IDs
    MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(hostname, &len);

    // Get rank ID as a string
    ostringstream rank_str;
    rank_str << rank;

    /* Order of parameters:
     * 0 : program name (ignored)
     * 1 : netlogo_prog
     * 2 : experiment_name
     * 3 : model file
     * 4 : out file
     * 5-n : setup files
     */
    // NOTE: Assume 1 process per setup file
    // NOTE: Only processes that have a setup file will run NetLogo
    if ((argc > (numtasks + 5)) || (argc < 6)) {
        if (rank == 0) {
            cout << "ERROR: incorrect number of parameters" << endl;
            cout << "Usage: " + string(argv[0]) + " [netlogo_prog] [experiment_name] [model_file] [output_file] [setup_file1 setup_file2 ...]" << endl;
        }
    } else if (argc > (rank + 5)) {

        // Max memory for NetLogo
        const string max_memory("16384m");

        // NetLogo program (.jar)
        const string netlogo_prog(argv[1]);

        // Experiment name
        string exp_name(argv[2]);
        exp_name = exp_name + "-" + rank_str.str();

        // Model file
        const string model_file(argv[3]);

        // Create partial output file based on rank ID
        string out_file(argv[4]);
        size_t ipos = out_file.find_last_of(".");
        out_file.insert(ipos, "-" + rank_str.str());

        // Setup file
        const string setup_file(argv[rank + 5]);

        // Pretty print configuration
        cout << hostname << "(" + rank_str.str() + "): " + exp_name + ", " + model_file + ", " + setup_file + ", " + out_file << endl;

        const string cmd("java -Xmx" + max_memory + " -Dfile.encoding=UTF-8 -cp " + netlogo_prog + " org.nlogo.headless.Main --experiment " + exp_name + " --model " + model_file + " --setup-file " + setup_file + " --table " + out_file);

        //cout << cmd << endl;
        system(cmd.c_str());
    } else {
        cout << hostname << "(" + rank_str.str() + "): no setup file assigned" << endl;
    }

    MPI_Finalize();

    return 0;
}
