import logging
import logging.config
import os
import sys

import structlog
from structlog.types import Processor

from src.settings import Settings


def init_logging(settings: Settings) -> None:
    settings.LOG_ROOT.mkdir(exist_ok=True)
    if not os.path.exists(filepath := settings.LOG_ROOT / settings.LOGGER_NAME):
        filepath.touch()

    processors: list[Processor] = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.ExtraAdder(),
    ]

    logging_dictconfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(
                        colors=False,
                        exception_formatter=structlog.dev.plain_traceback,
                    ),
                ],
                "foreign_pre_chain": processors,
            },
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(colors=True),
                ],
                "foreign_pre_chain": processors,
            },
        },
        "handlers": {
            "default": {
                "level": settings.LOG_FILE_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
            "file": {
                "level": settings.LOG_FILE_LEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(settings.LOG_ROOT, settings.LOGGER_NAME),
                "mode": "a",
                "maxBytes": settings.LOG_FILE_SIZE,
                "backupCount": settings.LOG_FILES_TO_KEEP,
                "encoding": "UTF-8",
                "formatter": "plain",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": settings.LOG_FILE_LEVEL,
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_dictconfig)

    structlog.configure(
        processors=processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    root_logger = logging.getLogger()

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.error(
            "An unexpected exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception
