import logging
import os
import sys
from pathlib import Path

import structlog

LOG_ROOT = Path(__file__).parent.parent.parent / 'logs'


def init_logging(name: str = 'Root', filepath: Path = LOG_ROOT):

    filepath.mkdir(exist_ok=True)
    if not os.path.exists(filepath := filepath / 'log.log'):
        filepath.touch()

    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.LogfmtRenderer(),
            foreign_pre_chain=processors,
        )
    )
    file_handler = logging.FileHandler(filepath, 'w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=processors,
        )
    )

    logging.basicConfig(
        handlers=[
            stream_handler,
            file_handler
        ],
        level=logging.DEBUG
    )

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger(name)