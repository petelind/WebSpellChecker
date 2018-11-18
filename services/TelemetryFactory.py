import os
import logging, watchtower


def create(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name=name)
    logger.addHandler(watchtower.CloudWatchLogHandler(log_group='Typonator', stream_name='TyponatorLog'))
    return logger
