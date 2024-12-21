"""Custom middleware."""

import logging
import time

from django.db import connection

logger = logging.getLogger(__name__)


class DatabaseInstrumentationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with connection.execute_wrapper(DatabaseLogger()):
            return self.get_response(request)


class DatabaseLogger:
    def __call__(self, execute, sql, params, many, context):
        start = time.monotonic()
        try:
            return execute(sql, params, many, context)
        finally:
            duration = time.monotonic() - start
            logging.info(
                "(%.3f) %s; args=%s",
                duration,
                sql,
                params,
                extra={"duration": duration, "sql": sql, "params": params},
            )
