from batch_parser import BatchParser
from streaming_parser import StreamingParser


class Controller:

    PARSERS = {
        "batch": BatchParser,
        "streaming": StreamingParser
    }

    @classmethod
    def load_parser(cls, logger, **kwargs):

        parser_type = kwargs.pop("execution_type")

        return cls.PARSERS[parser_type](logger, **kwargs)
