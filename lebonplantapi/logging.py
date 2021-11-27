import logging
import logging.config
import sys


def configure_logging(log_level: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level))
