from django.core.management.base import BaseCommand
from apis_backend.dbServices.connection import Base, engine

class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **kwargs):
        Base.metadata.create_all(bind=engine)
        self.stdout.write(self.style.SUCCESS('Database initialized'))
