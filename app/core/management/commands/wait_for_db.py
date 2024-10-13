"""
Django command to wait for the database to be available.
"""
from time import sleep

from typing import Any

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Wait for database to start"

    def handle(self, *args: Any, **options: Any) -> None:
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError, CommandError):
                self.stdout.write('Database unavailibale, waiting 1 second ...')
                sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
