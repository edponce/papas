#!/usr/bin/env python3


"""PaPaSParser: INI-based Format

This section provides the specification for PaPaSParser, used in both
configuration files and task parameter descriptions. This specification
is an extension of the INI format and uses a combination of dictionaries
and lists.

* A PaPaSParser implementation consists of tasks (or sections), identified
  by a '[task]' (or '[section]') header, and followed by up to two levels
  of 'name/value' entries. That is, the first set of values can themselves
  be a pair of 'name/value' entries.

* '[task]' (or '[section]') should not contain any whitespace to its left,
  that is, it should start at the first column of a line.

* The delimiter for 'name/value' entries is the colon character (':').

* The first level of 'names' should not contain any whitespace to its left,
  that is, it should start at the first column of a line.

* Indentation, tabs or whitespace, is used to make a 'value' pertain to a
  particular 'name'.

* A 'name' can be specified using any alphanumeric character, [0-9a-zA-Z].

* Predefined 'names' are:
    * 'name' - string describing the task
    * 'environ' - dictionary of environment variables, 'names' are the actual
                  names of the environment variables.
                  They are set automaticatically, do not include in 'command'.
    * 'command' - string representing the command line to run
    * 'after' - list of tasks dependencies, prerequisites
    * 'infiles' - dictionary of input files, 'names' are arbitrary
    * 'outfiles' - dictionary of output files, 'names' are arbitrary

* A 'task' is identified by the mandatory 'name/value' pair: 'command'.
  A 'section' does not have the 'command' 'name/value' pair.

* Inter-task interpolation using '${...}' syntax is allowed using 'values'
  from both levels of entries, '${name}' and '${name:value}'.

* Intra-task interpolation using '${...}' syntax is allowed using 'values'
  from both levels of entries, '${task:name}' and '${task:name:value}'.

* A single-line comment is a line that starts with a hash sign, '#'.


Example
=======

# This example describes two tasks, one called 'hello' that executes the
# program 'helloWorld.py' twice due to interpolation of values given in
# 'xparam'. The second task is called 'hello2' and has the same execution
# model as task 'hello'. Note that intra-task and inter-task interpolation
# are used to specify 'values' and it executes after task 'hello'.

[hello]
name: Hello world example
program: examples/helloWorld/helloWorld.py
cmdargs:
    xparam:
        10
        30
command: ${program} --xparam ${cmdargs:xparam}


[hello2]
name: Hello world example 2
program: ${hello:program}
cmdargs:
    xparam: ${hello:cmdargs:xparam}
command: ${program} --xparam ${cmdargs:xparam}
after:
    hello
"""


"""PaPaSParser: YAML Format (recommended)

This section provides the specification for PaPaSParser, used in both
configuration files and task parameter descriptions. This specification
follows the YAML format which is based on dictionaries and lists.

* This specification gets YAML ideas from Ansible:
  http://docs.ansible.com/ansible/latest/YAMLSyntax.html

* A PaPaSParser implementation consists of tasks (or sections), identified
  by a dictionary with the 'task' (or 'section') as the only key, and followed
  by up to two levels of 'name/value' entries. That is, the first set of
  values can themselves be a pair of 'name/value' entries.

* The delimiter for 'name/value' entries is the colon character (':').

* Indentation, tabs or whitespace, is used to make a 'value' pertain to a
  particular 'name'.

* A 'name' can be specified using any alphanumeric character, [0-9a-zA-Z].

* Predefined 'names' are:
    * 'name' - string describing the task
    * 'environ' - dictionary of environment variables, 'names' are the actual
                  names of the environment variables.
                  They are set automaticatically, do not include in 'command'.
    * 'command' - string representing the command line to run
    * 'after' - list of tasks dependencies, prerequisites
    * 'infiles' - dictionary of input files, 'names' are arbitrary
    * 'outfiles' - dictionary of output files, 'names' are arbitrary

* A 'task' is identified by the mandatory 'name/value' pair: 'command'.
  A 'section' does not have the 'command' 'name/value' pair.

* Inter-task interpolation using '${...}' syntax is allowed using 'values'
  from both levels of entries, '${name}' and '${name:value}'.

* Intra-task interpolation using '${...}' syntax is allowed using 'values'
  from both levels of entries, '${task:name}' and '${task:name:value}'.

* A single-line comment is a line that starts with a hash sign, '#'.


Example
=======

hello:
    name: Hello world example
    program: example/helloWorld/helloWorld.py
    cmdargs:
        xparam:
            - 10
            - 30
    command: ${program} --xparam ${cmdargs:xparam}


hello2:
    name: Hello world example 2
    program: ${hello:program}
    cmdargs:
        xparam: ${hello:cmdargs:xparam}
    environ:
        OMP_NUM_THREADS:
            - 2
            - 4
            - 8
    command: ${program} --xparam ${cmdargs:xparam}
    after:
        - hello
"""


"""PaPaSParser: JSON Format

This section provides the specification for PaPaSParser, used in both
configuration files and task parameter descriptions. This specification
follows the JSON format which is based on dictionaries and lists.

* A PaPaSParser implementation consists of tasks (or sections), identified
  by a dictionary with the 'task' (or 'section') as the only key, and followed
  by up to two levels of 'name/value' entries. That is, the first set of
  values can themselves be a pair of 'name/value' entries.

* The delimiter for 'name/value' entries is the colon character (':').

* A 'name' can be specified using any alphanumeric character, [0-9a-zA-Z].

* Predefined 'names' are:
    * 'name' - string describing the task
    * 'environ' - dictionary of environment variables, 'names' are the actual
                  names of the environment variables.
                  They are set automaticatically, do not include in 'command'.
    * 'command' - string representing the command line to run
    * 'after' - list of tasks dependencies, prerequisites
    * 'infiles' - dictionary of input files, 'names' are arbitrary
    * 'outfiles' - dictionary of output files, 'names' are arbitrary

* A 'task' is identified by the mandatory 'name/value' pair: 'command'.
  A 'section' does not have the 'command' 'name/value' pair.

* Inter-task interpolation using '${...}' syntax is allowed using 'values'
  from both levels of entries, '${name}' and '${name:value}'.

* Intra-task interpolation using '${...}' syntax is allowed using 'values'
  from both levels of entries, '${task:name}' and '${task:name:value}'.

* Comments are not allowed, use a dummy 'name/value' pair.


Example
=======

{
    "hello": {
        "name": "Hello world example",
        "program": "examples/helloWorld/helloWorld.py",
        "cmdargs": {
            "xparam": [10, 30]
        },
        "command": "${program} --xparam ${cmdargs:xparam}"
    },

    "hello2": {
        "name": "Hello world example 2",
        "program": "${hello:program}",
        "cmdargs": {
            "xparam": "${hello:cmdargs:xparam}"
        },
        "environ": {
            "OMP_NUM_THREADS": [2, 4, 8]
        },
        "command": "${program} --xparam ${cmdargs:xparam}",
        "after": ["hello"]
    }
}
"""


# import itertools
# import os
# import re
# import sys
# import collections
# import re


__all__ = ['PaPaSParser']


class PaPaSParser():

    papas_language = {
        'name': str,
        'program': str,
        'command': str,
        'cmdargs': dict,
        'cmdargs_': list,
        'after': list,
        'environ': dict,
        'environ_': list,
        'files': dict,
        'files_': list
    }
