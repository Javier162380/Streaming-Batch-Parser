import pytest

from src.streaming_parser import clean_message
from src.streaming_parser import process_events_batch


def test_clean_message():

    message = "12123131 asdaws asde\n"

    expected_message = ['12123131', "asdaws", "asde"]

    output_message = clean_message(message)

    assert expected_message == output_message

    message = "12123131 asdaws asde"

    expected_message = ['12123131', "asdaws", "asde"]

    output_message = clean_message(message)

    assert expected_message == output_message


def test_process_events_batch():

    batch = ["12123131 asdaws asde\n",
             "12123131 asdaws ergo\n",
             "12123131 ingo asdaws\n",
             "12123131 luko ingo\n"]

    expected_results = {
        "host_counter": {"asdaws": 2, "ingo": 1, "luko": 1},
        "input_host": ["asde", "ergo"],
        "output_host": ["ingo"]
    }

    results = process_events_batch(batch, "asdaws")

    assert results == expected_results


def test_process_invalid_events_batch():

    batch = ["12123131 asdaws asde\n",
             "12123131 asdaws ergo\n"
             "12123131 ingo asdaws\n",
             "12123131 luko ingo\n"]

    with pytest.raises(ValueError):
        process_events_batch(batch, "ingo")
