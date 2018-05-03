#!/usr/bin/env python3


from utils.logger import logger


def validate_file(fn, *, dir=False, read=True, write=False, execute=False):
    """Check access properties of a given file or directory, if it exists
    Only checks for properties that are set to True, others are ignored.

    Args:
        fn (str): File or directory to check
        dir (bool, optional): Specify if it is a file or directory
            (default is False)
        read (bool, optional): Check if path is readable
            (default is True)
        write (bool, optional): Check if path is writeable
            (default is False)
        execute (bool, optional): Check if path is executable
            (default is False)

    Returns:
        bool: True if all properties set are supported, else False

    Todo:
        * Remove print messages, useful for debugging only
    """
    prop_msg = []
    if not dir and not os.path.isfile(fn):
        prop_msg += ['file does not exists']
    elif dir and not os.path.isdir(fn):
        prop_msg += ['directory does not exists']
    else:
        if read and not os.access(fn, os.R_OK):
            prop_msg += ['is not readable']
        if write and not os.access(fn, os.W_OK):
            prop_msg += ['is not writable']
        if execute and not os.access(fn, os.X_OK):
            prop_msg += ['is not executable']

    if prop_msg:
        logger.error("'%s' %s" % (fn, ', '.join(prop_msg)))
        return False
    return True
