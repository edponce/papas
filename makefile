# C++ MPI compiler
CXX := mpicxx

# Compiler and linker options
CXXFLAGS :=

# Preprocessor definitions
DEFINES :=

# Specify non-standard header paths
INCDIR :=

# Specify non-standard library paths
LIBDIR :=

# Specify libraries to link
LIBS :=

# Main driver and executable
DRIVER := netlogo_mpi.cpp
EXE := netlogo_mpi

###############################################################################
# Targets that are not real files
.PHONY: all clean

all:
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCDIR) $(LIBDIR) $(DRIVER) -o $(EXE) $(LIBS)

clean:
	rm -f $(EXE) 
