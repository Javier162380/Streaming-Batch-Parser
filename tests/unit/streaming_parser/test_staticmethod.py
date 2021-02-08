

def test_aggregate_hosts(streaming_parser_instance):

    host_counter = {"Adva": 2, "ferka": 5}

    streaming_parser_instance.host_aggregate = {"Adva": 1}

    streaming_parser_instance.aggregate_hosts(streaming_parser_instance.host_aggregate, host_counter)

    assert streaming_parser_instance.host_aggregate == {"Adva": 3, "ferka": 5}


def test_aggregate_target_host_connections(streaming_parser_instance):

    hostname_received = ["Adva", "adva", "ferka", "Adva"]

    streaming_parser_instance.aggregate_target_host_connections(
        streaming_parser_instance.hostnames_received, hostname_received)

    assert streaming_parser_instance.hostnames_received == set(["Adva", "adva", "ferka"])


def test_get_higher_host(streaming_parser_instance):

    streaming_parser_instance.host_aggregate = {"Adva": 1, "feka": 234, "dunno": 45}

    results = streaming_parser_instance.get_higher_host(streaming_parser_instance.host_aggregate)

    assert results[0] == "feka"
    assert results[1] == 234
