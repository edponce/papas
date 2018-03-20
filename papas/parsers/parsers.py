#!/usr/bin/env python3


# import itertools
# import os
# import re
# import sys
# import collections
# import re


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
