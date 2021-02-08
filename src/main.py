import sys
import logging

from cli import cli
from controller import Controller


def main():

    params = cli(sys.argv[1:])

    logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout,
                        format="%(asctime)s [%(threadName)-12.12s] "
                        "[%(levelname)-5.5s]  %(message)s")
    logger.setLevel(logging.DEBUG if params['verbose'] else logging.INFO)
    logger.debug(f"Execution trigger with the following params {params}")

    parser_instance = Controller.load_parser(logger, **params)
    parser_instance.execute()


if __name__ == "__main__":
    main()
