import logging

import pytest

from src.batch_parser import BatchParser
from src.streaming_parser import StreamingParser


@pytest.fixture()
def batch_parser_instance():

    logger = logging.getLogger()

    return BatchParser(
        logger=logger,
        start_time=1565650074799,
        end_time=1565650190664,
        file_path='unit/batch_parser/fixtures/input-file-100.txt',
        host_name='Roxanna',
        batch_size=10)


@pytest.fixture()
def streaming_parser_instance():

    logger = logging.getLogger()

    return StreamingParser(
        queue_size=10000000,
        time=36000,
        batch_size=1000,
        logger=logger,
        host_name='Ayurbeda',
        target_directory='unit/streaming_parser/fixtures'
    )
