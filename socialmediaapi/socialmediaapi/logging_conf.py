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
                },
                "handlers": {
                    "default": {
                        "class": "rich.logging.RichHandler",
                        "level": "DEBUG",
                        "formatter": "console",
                    },
                },
                "loggers": {
                    "social": {
                        "handlers": ["default"],
                        "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                        "propagate": False,  # Prevents double logging sent to root logger
                    },
                },
            }
        )
    except Exception as e:
        print(f"Error configuring logging: {e}")
        raise

    print("Logging configured successfully")
