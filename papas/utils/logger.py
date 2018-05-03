#!/usr/bin/env python3


import logging


def get_logger(name):
    """Generate a logging object"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - '
                                       '%(levelname)s - %(message)s',
                                       datefmt='%Y-%m-%d %H:%M:%S')

    log_file_handler = logging.FileHandler(name + '.log')
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)

    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setLevel(logging.INFO)
    log_stream_handler.setFormatter(formatter)
    logger.addHandler(log_stream_handler)

    return logger


logger = get_logger('papas')
