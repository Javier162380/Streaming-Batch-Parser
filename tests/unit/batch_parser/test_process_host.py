
def test_process_host(batch_parser_instance):

    batch = [
        '1565647204351 Keimy Matina\n', '1565647205599 Keimy Dmetri\n', '1565647212986 Tyreonna Rehgan\n',
        '1565647228897 Heera Eron\n', '1565647246869 Jeremyah Morrigan\n', '1565647247170 Khiem Tailee\n',
        '1565647256008 Remiel Jadon\n', '1565647260788 Monet Jarreth\n', '1565647264445 Jil Cerena\n',
        '1565647268712 Keimy Kallan'
    ]

    batch_parser_instance.host_name = 'Keimy'
    batch_parser_instance.start_time = 1565647204351
    batch_parser_instance.end_time = 1565647260788
    hosts = batch_parser_instance.process_hosts(batch)

    assert hosts == ['Matina', 'Dmetri']

    batch_parser_instance.end_time = 1565647268715
    hosts = batch_parser_instance.process_hosts(batch)

    assert hosts == ['Matina', 'Dmetri', 'Kallan']
