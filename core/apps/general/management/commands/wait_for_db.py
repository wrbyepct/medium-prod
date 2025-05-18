"""Command for probing DB."""

# ruff: noqa: ARG002
import sys
import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to wait for the database to be available."""

    def handle(self, *args, **options):
        """Probe for PostGres avaiability, after 30 secs report error."""
        self.stdout.write("Waiting for PostgreSQL to become available...")
        suggest_unrecoverable_after = 30
        start = time.time()
        while True:
            try:
                conn = connections["default"]
                conn.cursor()
                break
            except (Psycopg2OpError, OperationalError) as e:
                sys.stdout.write("Waiting for PostgreSQL to become available...\n")
                if time.time() - start > suggest_unrecoverable_after:
                    sys.stderr.write(
                        f"This is taking longer than expected, the following exception may be indicative of an unrecoverable error: '{e}'\n"
                    )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("PostgreSQL is available."))
