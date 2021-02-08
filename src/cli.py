import argparse
import typing


def cli(*args) -> typing.Dict:

    parser = argparse.ArgumentParser(
        description="Host processor"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity",
        action="store_true"
    )

    # SUBPARSERS.
    subparser = parser.add_subparsers(title="execution-mode")

    batch_subparser = subparser.add_parser("batch", parents=[parser], add_help=False)
    streaming_subparser = subparser.add_parser("streaming", parents=[parser], add_help=False)
    batch_subparser.set_defaults(execution_type="batch")
    streaming_subparser.set_defaults(execution_type="streaming")

    # BATCHPROCESSOR arguments.
    batch_subparser.add_argument(
        "-H",
        "--host-name",
        help="Host Name we are analyzing",
        required=True
    )

    batch_subparser.add_argument(
        "-s",
        "--start-time",
        help="Start time of the execution",
        required=True,
        type=int
    )

    batch_subparser.add_argument(
        "-e",
        "--end-time",
        help="End time of the execution",
        required=True,
        type=int
    )

    batch_subparser.add_argument(
        "-f",
        "--file-path",
        help="File abs path where the log file is located",
        required=True,
        type=str
    )

    batch_subparser.add_argument(
        "-b",
        "--batch-size",
        help="Size of the batch for processing data",
        type=int,
        required=False,
        default=1064
    )

    # Streaming Proccesor Argument.

    streaming_subparser.add_argument(
        "-q",
        "--queue-size",
        help="Max number of messages retain by the qeue",
        type=int,
        default=10000000
    )

    streaming_subparser.add_argument(
        "-b",
        "--batch-size",
        help="Size of the batch for proccessing data",
        type=int,
        required=False,
        default=1064
    )

    streaming_subparser.add_argument(
        "-t",
        "--time",
        help="Time in seconds while the qeue continue accept receiving events",
        type=int,
        default=3600

    )

    streaming_subparser.add_argument(
        "-T",
        "--target-directory",
        help="Target directory where files are located",
        type=str
    )

    streaming_subparser.add_argument(
        "-H",
        "--host-name",
        help="Host Name we are analyzing",
        required=True
    )

    return parser.parse_args(*args).__dict__
