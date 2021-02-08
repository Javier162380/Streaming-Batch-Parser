import os
from src.batch_parser import BatchParser

file_abs_path = os.path.join(
    os.path.dirname(__file__), 'fixtures/input-file-10.txt')


def test_execute_without_iteration(batch_parser_instance, mocker):
    mocker.patch.object(BatchParser, 'process_batch')

    batch_parser_instance.file_path = file_abs_path
    batch_parser_instance.start_time = 1165647204351
    batch_parser_instance.end_time = 1185647247169

    batch_parser_instance.execute()

    assert BatchParser.process_batch.call_count == 0


def test_execute_with_multiple_iteration(batch_parser_instance, mocker):
    mocker.patch.object(BatchParser, 'process_batch')

    batch_parser_instance.file_path = file_abs_path
    batch_parser_instance.start_time = 1165647204351
    batch_parser_instance.end_time = 1865647204351
    batch_parser_instance.batch_size = 3

    batch_parser_instance.execute()

    assert BatchParser.process_batch.call_count == 4


def test_execute_with_multiple_iteration_skipping_one(batch_parser_instance, mocker):
    mocker.patch.object(BatchParser, 'process_batch')

    batch_parser_instance.file_path = file_abs_path
    batch_parser_instance.start_time = 1565647228897
    batch_parser_instance.end_time = 1865647204351
    batch_parser_instance.batch_size = 3

    batch_parser_instance.execute()

    assert BatchParser.process_batch.call_count == 3
