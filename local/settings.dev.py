import colorlog


class CustomFormatter(colorlog.ColoredFormatter):
    def format(self, record):  # noqa: A003
        # Get the original log_color
        record.levelpad = " " * (10 - len(record.levelname))  # customized record field
        return super().format(record)


LOGGING["formatters"]["verbose"]["()"] = CustomFormatter  # type: ignore # noqa: F821
