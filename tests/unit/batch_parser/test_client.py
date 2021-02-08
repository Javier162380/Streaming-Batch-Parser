

def test_client(batch_parser_instance):

    assert batch_parser_instance.start_time == 1565650074799
    assert batch_parser_instance.end_time == 1565650190664
    assert batch_parser_instance.file_path == 'unit/batch_parser/fixtures/input-file-100.txt'
    assert batch_parser_instance.host_name == 'Roxanna'
    assert batch_parser_instance.batch_size == 10
