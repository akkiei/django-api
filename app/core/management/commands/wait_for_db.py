import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ cmd to pause exec til db is available"""

    def handle(self, *args, **options):
        self.stdout.write(" waiting to db to initialize ...")
        db_con = None
        while not db_con:
            try:
                db_con = connections['default']
            except OperationalError:
                self.stdout.write(" db unavailable, wait for 1 second ...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS(" db init successfully. "))
