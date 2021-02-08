from src.batch_parser import BatchParser


def test_proccess_full_batch(batch_parser_instance, mocker):
    mocker.patch.object(BatchParser, 'process_hosts')
    batch = [
        '1565647204351 Keimy Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n',
        '1565647268712 Keimy Kallan'
    ]

    batch_analysis = {
        "start_batch_time": 1565647204351,
        "end_batch_time": 1565647268712,
        "pivot": 5,
        "middle_batch_time": 1565647247170
    }

    batch_parser_instance.start_time = 1565647204351
    batch_parser_instance.end_time = 1565647268712

    batch_parser_instance.process_batch(batch=batch, batch_analysis=batch_analysis)

    BatchParser.process_hosts.assert_called_once_with(batch)


def test_process_half_lower_batch(batch_parser_instance, mocker):
    mocker.patch.object(BatchParser, 'process_hosts')
    batch = [
        '1565647204351 Keimy Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n',
        '1565647268712 Keimy Kallan'
    ]

    batch_analysis = {
        "start_batch_time": 1565647204351,
        "end_batch_time": 1565647268712,
        "pivot": 5,
        "middle_batch_time": 1565647247170
    }

    batch_parser_instance.start_time = 1565647204351
    batch_parser_instance.end_time = 1565647247169

    batch_parser_instance.process_batch(batch=batch, batch_analysis=batch_analysis)

    BatchParser.process_hosts.assert_called_once_with(batch[:batch_analysis["pivot"]])


def test_process_half_upper_batch(batch_parser_instance, mocker):
    mocker.patch.object(BatchParser, 'process_hosts')
    batch = [
        '1565647204351 Keimy Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n',
        '1565647268712 Keimy Kallan'
    ]

    batch_analysis = {
        "start_batch_time": 1565647204351,
        "end_batch_time": 1565647268712,
        "pivot": 5,
        "middle_batch_time": 1565647247170
    }

    batch_parser_instance.start_time = 1565647247170
    batch_parser_instance.end_time = 1865647268715

    batch_parser_instance.process_batch(batch=batch, batch_analysis=batch_analysis)

    BatchParser.process_hosts.assert_called_once_with(batch[batch_analysis["pivot"]:])
