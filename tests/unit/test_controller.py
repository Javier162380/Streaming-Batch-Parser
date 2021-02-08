import logging
import logging
import pytest

from src.base import BaseParser
from src.controller import Controller

logger = logging.getLogger()


@pytest.mark.parametrize("params", [{
    "start_time": 102312412412,
    "end_time": 102312412412,
    "host_name": "thehost",
    "execution_type": "batch",
    "file_path": "myfile",
    "batch_size": 1064,
    "logger": logger
}, {
    "start_time": 102312412412,
    "end_time": 102312412412,
    "host_name": "thehost",
    "execution_type": "batch",
    "file_path": "myfile",
    "batch_size": 1065,
    "logger": logger
}])
def test_controller_correct_load(params):

    batch_parser_instance = Controller.load_parser(**params)


@pytest.mark.parametrize("params", [{
    "start_time": 102312412412,
    "end_time": 102312412412,
    "host_name": "thehost",
    "execution_type": "dummyparser",
    "file_path": "myfile",
    "batch_size": 1064,
    "logger": logger
}, {
    "start_time": 102312412412,
    "end_time": 102312412412,
    "host_name": "thehost",
    "file_path": "myfile",
    "batch_size": 1065,
    "logger": logger
}])
def test_controller_invalid_load(params):

    with pytest.raises(KeyError):
        batch_parser_instance = Controller.load_parser(**params)
