import os

import pytest


@pytest.mark.parametrize("host_name, expected_host_name",
                         [('Roxxanna\n', 'Roxxanna'),
                          ('Roxxana', 'Roxxana')])
def test_clean_host(host_name, expected_host_name, batch_parser_instance):

    output = batch_parser_instance.clean_host(host_name)

    assert output == expected_host_name


def test_proccess_file_per_batches(batch_parser_instance):
    file_abs_path = os.path.join(
        os.path.dirname(__file__), 'fixtures/input-file-10.txt')
    batches = list(batch_parser_instance.process_file_per_batches(file_path=file_abs_path,
                                                                  batch_size=9))

    assert len(batches) == 2
    assert batches[0] == [
        '1565647204351 Aadvik Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n']
    assert batches[1] == ['1565647268712 Naetochukwu Kallan']

    batches = list(batch_parser_instance.process_file_per_batches(file_path=file_abs_path,
                                                                  batch_size=10))

    assert len(batches) == 1
    assert batches[0] == [
        '1565647204351 Aadvik Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n',
        '1565647268712 Naetochukwu Kallan']


def test_analyze_batch(batch_parser_instance):

    batch = [
        '1565647204351 Aadvik Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n',
        '1565647268712 Naetochukwu Kallan']

    batch_analysis = batch_parser_instance.analyze_batch(batch)

    assert batch_analysis["start_batch_time"] == 1565647204351
    assert batch_analysis["end_batch_time"] == 1565647268712
    assert batch_analysis["pivot"] == 5
    assert batch_analysis["middle_batch_time"] == 1565647247170

    batch = [
        '1565647204351 Aadvik Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n'
    ]

    batch_analysis = batch_parser_instance.analyze_batch(batch)

    assert batch_analysis["start_batch_time"] == 1565647204351
    assert batch_analysis["end_batch_time"] == 1565647264445
    assert batch_analysis["pivot"] == 4
    assert batch_analysis["middle_batch_time"] == 1565647246869
