import sys

import pytest
sys.path.append('src/')
from cli import cli

CLI_INPUT = ([
    "batch",
    "--host-name", "thehost",
    "--start-time", "102312412412",
    "--end-time", "102312412412",
    "--file-path", "myfile"
], [
    "batch",
    "-H", "thehost",
    "-s", "102312412412",
    "-e", "102312412412",
    "-f", "myfile",
    "-b", "1065",
    "-v"
], [
    "streaming",
    "--target-directory", "data/streaming",
    "--host-name", "rabat"
])

CLI_OUTPUT = ({
    "start_time": 102312412412,
    "end_time": 102312412412,
    "host_name": "thehost",
    "execution_type": "batch",
    "file_path": "myfile",
    "batch_size": 1064,
    "verbose": False,
}, {
    "start_time": 102312412412,
    "end_time": 102312412412,
    "host_name": "thehost",
    "execution_type": "batch",
    "file_path": "myfile",
    "batch_size": 1065,
    "verbose": True
}, {
    "execution_type": "streaming",
    "time": 3600,
    "target_directory": "data/streaming",
    "host_name": "rabat",
    "batch_size": 1064,
    "queue_size": 10000000,
    "verbose": False
})

CLI_UNEXPECTED_INPUT = (["--start-time", "123123123", "--end-time", "1232321312"])


@pytest.mark.parametrize("cli_input,expected_output", zip(CLI_INPUT, CLI_OUTPUT))
def test_cli_with_expected_parameters(cli_input, expected_output):

    cli_output = cli(cli_input)

    assert cli_output == expected_output


@pytest.mark.parametrize("cli_unexpected_input", CLI_UNEXPECTED_INPUT)
def test_cli_with_unexpected_parameters(cli_unexpected_input):

    with pytest.raises(SystemExit):
        cli(cli_unexpected_input)
