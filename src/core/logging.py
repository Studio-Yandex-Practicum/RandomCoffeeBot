import logging
import os
import sys

import structlog

from src.settings import Settings


def init_logging(settings: Settings):
    settings.LOG_ROOT.mkdir(exist_ok=True)
    if not os.path.exists(filepath := settings.LOG_ROOT / settings.LOGGER_NAME):
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
    file_handler = logging.FileHandler(filepath, "w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=processors,
        )
    )

    logging.basicConfig(handlers=[stream_handler, file_handler], level=settings.LOG_MIN_ERROR_LEVEL)

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        cache_logger_on_first_use=True,
    )
