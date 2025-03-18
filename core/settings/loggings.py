# type: ignore
"""Loggings settings."""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # Name of the formmater
        "standard": {
            "format": "{asctime} {name} {levelname} {message}",
            "style": "{",
        },
        "verbose": {
            "()": "colorlog.ColoredFormatter",
            "format": "{asctime}:{log_color}[{levelname}] | {name} {module}.py (line {lineno:d}) | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": [],
        },
    },
    "loggers": {
        logger_name: {
            "level": "INFO",
            "propagate": True,
        }
        for logger_name in (
            "django",
            "django.request",
            "django.template",
            "django.db.backends",
            "core",
        )
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}
