from logging.config import dictConfig

from socialmediaapi.config import DevConfig, config


def configure_logging() -> None:
    try:
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "console": {
                        "class": "logging.Formatter",
                        "datefmt": "%Y-%m-%d %H:%M:%S",
                        "format": "%(name)s:%(lineno)d - %(message)s",
                    },
                    "file": {
                        "class": "logging.Formatter",
                        "datefmt": "%Y-%m-%d %H:%M:%S",
                        "format": "%(asctime)s.%(msecs)03dz | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
                    },
                },
                "handlers": {
                    "default": {
                        "class": "rich.logging.RichHandler",
                        "level": "DEBUG",
                        "formatter": "console",
                    },
                    "rotating_file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "DEBUG",
                        "formatter": "file",
                        "filename": "socialmediaapi.log",
                        "maxBytes": 1024 * 1024,  # 1MB
                        "backupCount": 5,
                        "encoding": "utf8",
                    },
                },
                "loggers": {
                    "uvicorn": {
                        "handlers": ["default", "rotating_file"],
                        "level": "INFO",
                    },
                    "socialmediaapi": {
                        "handlers": ["default", "rotating_file"],
                        "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                        "propagate": False,  # Prevents double logging sent to root logger
                    },
                    "databases": {
                        "handlers": ["default"],
                        "level": "WARNING",
                    },
                    "aiosqlite": {
                        "handlers": ["default"],
                        "level": "WARNING",
                    },
                },
            }
        )
    except Exception as e:
        print(f"Error configuring logging: {e}")
        raise

    print("Logging configured successfully")
