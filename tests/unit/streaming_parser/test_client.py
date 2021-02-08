

def test_client(streaming_parser_instance):

    assert streaming_parser_instance.queue_size == 10000000
    assert streaming_parser_instance.time == 36000
    assert streaming_parser_instance.host_name == 'Ayurbeda'
    assert streaming_parser_instance.processed_directory == 'unit/streaming_parser/fixtures/processed'
