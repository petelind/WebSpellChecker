import os
import logging, watchtower

from boto3 import Session


def create(name):
    logging.basicConfig(level=logging.INFO)
    AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('ACCESS_KEY')
    AWS_REGION_NAME = 'us-east-1'

    boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION_NAME)
    logger = logging.getLogger(name=name)
    logger.addHandler(watchtower.CloudWatchLogHandler(log_group='Typonator', stream_name='TyponatorLog', boto3_session=boto3_session))
    return logger
