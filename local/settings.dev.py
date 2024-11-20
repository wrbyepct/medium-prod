"""Setting for dev perference."""  # noqa: INP001

import colorlog


class CustomFormatter(colorlog.ColoredFormatter):
    """Custom logging formatter."""

    def format(self, record):  # noqa: D102, ANN001
        # Get the original log_color
        record.levelpad = " " * (10 - len(record.levelname))  # customized record field
        return super().format(record)


LOGGING["formatters"]["verbose"]["()"] = CustomFormatter  # type: ignore
