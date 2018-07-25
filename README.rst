.. highlight:: shell


.. image:: https://travis-ci.org/edponce/papas.svg?branch=master
   :target: https://travis-ci.org/edponce/papas

.. image:: https://coveralls.io/repos/github/edponce/papas/badge.svg?branch=master
   :target: https://coveralls.io/github/edponce/papas?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/edponce/papas


=========
IMPORTANT
=========

PaPaS is a work-in-progress and not ready for general use...yet.
If you have questions or comments please contact Eduardo Ponce at eponcemo@utk.edu.


============
INTRODUCTION
============

The current landscape of scientific research is widely based on
modeling and simulation, typically with complexity in the simulation's
flow of execution and parameterization properties.
Execution flows are not necessarily
straightforward since they may need multiple processing tasks and iterations.
Furthermore, parameter and performance studies are common approaches used
to characterize a simulation, often requiring traversal of a large parameter space.
High-performance computers offer practical resources
at the expense of users handling the setup, submission, and management of jobs.
This work presents the design of PaPaS, a portable, lightweight, and generic
workflow framework for conducting parallel parameter and performance studies.
Workflows are defined using parameter files based on keyword-value pairs syntax,
thus removing from the user the overhead of creating complex scripts to manage the workflow.
A parameter set consists of any combination of environment variables,
files, partial file contents, and command line arguments.
PaPaS is being developed in Python 3 with support for distributed parallelization
using SSH, batch systems, and C++ MPI.
The PaPaS framework will run as user processes,
and can be used in single/multi-node and multi-tenant computing systems.
An example simulation using the BehaviorSpace tool from NetLogo and a matrix
multiply using OpenMP are presented as parameter and performance studies, respectively.
The results demonstrate that the PaPaS framework offers a simple method for defining
and managing parameter studies, while increasing resource utilization.


==================
PaPaS ARCHITECTURE
==================

The PaPaS framework is a collection of modular systems, each with unique
functionality and independent interfaces.
The primary system components are the
parameter study, workflow, cluster, and visualization
engines.

Parameter Study Engine
======================

A parameter study represents a set of workflows to be executed,
where a workflow corresponds to an instance having a unique parameter combination.
Users write a parameter file using a keyword-based workflow description language.
A workflow's description can be divided across multiple parameter files; this
allows composition and re-usability of task configurations.
Parameter files follow either YAML, JSON, or INI-like data serialization formats
with minor constraints.
The processing of these files consists of a parsing and syntax validation step,
followed by string interpolation for parameters that were specified with
multiple values.
The operation of interpolation identifies all the possible unique parameter
combinations and forwards this information to a workflow generator which in
turn spawns a workflow engine instance per combination.
Parameter study configurations are stored in a file database as part
of the monitoring activity.
PaPaS provides checkpoint-restart functionality in case of fault or a deliberate
pause/stop operation.
A parameter study's state can be saved in a workflow file and reloaded at a later time.
Another method of defining a parameter study is through the workflow
generator Python 3 interface.
This mechanism adds the hooks to embed PaPaS as a task of a larger user-defined
workflow.

Workflow Engine
===============

Workflow engines are a core component as they orchestrate the
execution of workflow instances.
The task generator takes a workflow description and constructs
a directed acyclic graph (DAG) where nodes correspond to indivisible tasks.
A task manager controls the scheduling and monitoring of tasks.
PaPaS runs easily on a local laptop or workstation.
For cluster systems, workflow tasks are delegated to the
cluster engine component.
Several factors affect scheduling heuristics such as task dependencies,
availability and capability of computing resources,
and the application(s) behavior.
A task profiler measures each task's runtime, but
currently this only serves as performance feedback to the user.
Workflow engine actions, task/workflow statistics, and logs are stored in a per-workflow
file storage database; this information is later used to include
provenance details at either workflow completion or a checkpoint.
A visualization engine enables access to a view of the workflow's DAG.
The workflow engine communicates the progression of states to the
visualization engine.

Cluster Engine
==============

The cluster engine is a component that serves as an interface for both
managed and unmanaged computer clusters.
A managed cluster is assumed to be used concurrently by multiple users
and makes use of a batch system (e.g., PBS, SGE),
while an unmanaged cluster is mostly single-user and has a SSH setup.
For managed clusters, the common approach is to submit a single task
per batch job.
Single task submissions are mainly applicable for applications that achieve
a high-utilization of computing resources or have long execution times, and
adding concurrent task executions hinder performance.
For single-node and single-core applications, submitting a
large number of jobs to a multi-tenant system may not necessarily be the best
approach.
PaPaS workflow and cluster engines enable grouping intra/inter-workflow
tasks as a single batch job.
The main mechanism for grouping tasks as single jobs is using a C++ MPI task dispatcher.
In some cases, task grouping increases the cluster's utilization efficiency, reduces
batch/scheduling operations, and improves turnaround time of jobs.

Visualization Engine
====================

The DAGs generated by the workflow engine are used to construct
visual graphs of the overall workflow as well as the current state of
the processing.
PaPaS utilizes a wrapper over PyGraphviz to build
and update graphs on-demand.
A workflow visualization can be viewed and exported in text or common image formats.
This capability can also be enabled as a validation method of the parameter study
configuration prior to any execution taking place.


=============================
WORKFLOW DESCRIPTION LANGUAGE
=============================

This section describes the workflow description language (WDL) specification used
by the PaPaS framework.
The PaPaS WDL consists of a set of keywords that
can describe individual tasks, task dependencies, parameter sets,
and general configurations.

PaPaS's WDL is based on a mix of lists and associative structures. As a consequence,
it is serializable and can be converted to common human-readable formats such as YAML, JSON, and INI.
Workflow descriptions are transformed into a common internal format.
The following is the general specification of rules for configuring parameter studies using YAML format.

- A parameter study consists of tasks (or sections), identified
  by a *task* (or *section*) as the only key, and followed
  by up to two levels of *keyword-value* entries. That is, the first set of
  values can themselves be a pair of *keyword-value* entries.
- The delimiter for *keyword-value* entries is the colon character.
- Indentation, tab or whitespace, is used to make a *value* pertain to a
  particular *keyword*.
- A single-line comment is a line that starts with a pound or hash symbol (#).
- A *keyword* can be specified using any alphanumeric character.
- All *keywords* are parsed as strings and *values* are inferred
  from written format.
- *Keywords* that are not predefined are considered as a user-defined
  *keywords* and can be used in value interpolations.
- Ranges with a step size are supported for numerical values using the notation *start:step:end*.
- A *task* is identified by the *command* keyword.
- Value interpolation uses a flat associative array syntax.
- Intra-task interpolation using ${*...*} syntax is allowed using *values* from both entry
  levels (e.g., ${*keyword*} and ${*keyword:value*}).
- Inter-task interpolation using ${*...*} syntax is allowed using *values* from both entry
  levels (e.g., ${*task:keyword*} and ${*task:keyword:value*}).

The list below presents a list of common keywords corresponding to PaPaS WDL:
- **command** - string representing the command line to run
- **name** - string describing the task
- **environ** - dictionary of environment variables where
  *keywords* are the actual names of the environment variables.
- **after** - list of tasks dependencies, prerequisites
- **infiles** - dictionary of input files, *keywords* are arbitrary
- **outfiles** - dictionary of output files, *keywords* are arbitrary
- **substitute** - used for interpolation of partial file contents. Expects a
  *keyword/value* pair where *keyword* is a Python 3 regular expression
  and *value* is a list of strings to be used instead.
- **parallel** - mode to use for parallelism, (e.g., ssh, MPI)
- **batch** - batch system of cluster (e.g., PBS)
- **nnodes** - number of nodes to use for a cluster job
- **ppnode** - number of task processes to run per nodes
- **hosts** - hostnames or IP addresses of compute nodes
- **fixed** - list of parameters to be fixed. All of these parameters need to have the
  same number of values to allow ordered one-to-one mappings.
- **sampling** - samples a subset of the parameter space based


===========
FUTURE WORK
===========

The PaPaS framework provides exciting support for computational and
data science users to achieve higher productivity.
Despite its capabilities, there are numerous extensions to PaPaS under consideration
to provide even more usability, flexibility, and productivity.
Future efforts are to integrate PaPaS workflows into grid workflow systems,
such as Taverna and Pegasus, to readily extend the potential PaPaS user community.
One potential approach is to allow the exchange of PaPaS task description files with
Pegasus and similar actively developed workflow management systems.
A PaPaS task internal representation can be converted to define a Pegasus workflow
via the Pegasus Python libraries for writing direct acyclic graphs in XML (DAX).
In this scheme, PaPaS would serve as a
front-end tool for defining parameter studies while leveraging a wide array of
features provided by the Pegasus framework.

Currently, the PaPaS design does not supports nor provides a mechanism to express
automatic aggregation of files, even if tasks utilize the same names for output
files.
Some difficulties that arise with automatic aggregation of files are content ordering
and parsing tasks correctly
(replicated file names). In order to support automatic aggregation,
additional keywords will need to be included in the PaPaS workflow language.

An additional feature to aid in workflow creation is to use a graphical interface
from which the user can define parameter studies. This extension can be designed
with capabilities to create, modify, and/or remove tasks from workflows, as well
as for viewing workflow graphs.

The PaPaS framework will be extended to support tools for measuring application
performance, in addition to the current runtime measures. One popular example of such tools
is PAPI.
The current design only measures the runtime of each parameter study workflow,
workflow instance, and task. Higher-detail of profiling metrics could be useful
for: (1) providing the user with additional profiling information, mainly
for benchmarking studies, and (2) as
feedback for improving workflow planning and scheduling decisions.


There is still work to investigate for managing and scheduling parameter
workflows. For example, consider a parameter workflow containing tasks with
same parameters and tasks with multi-valued parameters.
Then, the user may wish to dictate that the set of
workflows will follow a depth-first or breadth-first execution.

These kinds of additional features could significantly broaden the usefulness
and resultant productivity improvements provided by PaPaS.


.. NetLogo 6.0
.. ===========
.. 
.. The `Github repo`_ is in this link.
.. This project provides a workflow composed of a set of scripts and a MPI
.. dispatcher program that allows to run parallel jobs of NetLogo in a managed
.. cluster. The workflow was designed for large runs of parameter sweeping
.. using Behavior Space.
.. 
.. Python 3 scripts parse NetLogo GUI model files to identify and select available
.. experiments. The user specifies the parameters and parallel configuration
.. required in a cluster submission script (PBS). The job is submitted to the
.. cluster and a C++ MPI program distributes XML setup files among multiple
.. processes/nodes. Each process runs a subset of parameters/timesteps.
.. Partial output files are merged and reordered into a single CSV file for
.. further data analysis.
.. 
.. .. _Github repo: https://github.com/edponce/papas
.. 
.. 
.. NetLogo Workflow
.. ----------------
.. 
.. 1. User sets up model and parameters in NetLogo GUI (offline)
.. 2. Model file and cluster submission script are uploaded to the cluster
.. 3. User logs to cluster and submits job
.. 4. When job completes, user downloads output files
.. 
.. This work is currently under development for the ACF cluster at UTK.
.. 
.. NOTE: For test cases, create a symbolic link of the local NetLogo 6.0
.. top directory inside `mpi_netlogo` project ::
.. 
..     $ cd mpi_netlogo
..     $ ln -s /full/path/to/local/NetLogo NetLogo_6.0
