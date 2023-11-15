from django.core.management.base import BaseCommand
from core.models import Person, DataSource, Record


class Command(BaseCommand):
    help = "deletes all data from the database"

    def handle(self, *args, **kwargs):
        Record.objects.all().delete()
        DataSource.objects.all().delete()
        Person.objects.all().delete()

        self.stdout.write(f"Records: {len(Record.objects.all())}")
        self.stdout.write(f"Persons: {len(Person.objects.all())}")
        self.stdout.write(str(DataSource.objects.all()))
        self.stdout.write(self.style.WARNING("Database has been cleared"))
