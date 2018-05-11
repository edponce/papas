.. highlight:: shell

=========  ========  =======
Travis CI  Coverage  License
=========  ========  =======
.. image:: https://travis-ci.org/edponce/papas.svg?branch=master
   :target: https://travis-ci.org/edponce/papas

.. image:: https://coveralls.io/repos/github/edponce/papas/badge.svg?branch=master
   :target: https://coveralls.io/github/edponce/papas?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/edponce/papas
=========  ========  =======


======
README
======

NetLogo 6.0
===========

The `Github repo`_ is in this link.
This project provides a workflow composed of a set of scripts and a MPI
dispatcher program that allows to run parallel jobs of NetLogo in a managed
cluster. The workflow was designed for large runs of parameter sweeping
using Behavior Space.

Python 3 scripts parse NetLogo GUI model files to identify and select available
experiments. The user specifies the parameters and parallel configuration
required in a cluster submission script (PBS). The job is submitted to the
cluster and a C++ MPI program distributes XML setup files among multiple
processes/nodes. Each process runs a subset of parameters/timesteps.
Partial output files are merged and reordered into a single CSV file for
further data analysis.

.. _Github repo: https://github.com/edponce/papas


NetLogo Workflow
----------------

1. User sets up model and parameters in NetLogo GUI (offline)
2. Model file and cluster submission script are uploaded to the cluster
3. User logs to cluster and submits job
4. When job completes, user downloads output files

This work is currently under development for the ACF cluster at UTK.

NOTE: For test cases, create a symbolic link of the local NetLogo 6.0
top directory inside `mpi_netlogo` project ::

    $ cd mpi_netlogo
    $ ln -s /full/path/to/local/NetLogo NetLogo_6.0
