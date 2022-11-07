import factory
from django.core.management.base import BaseCommand
from django.db import transaction

from core.factories.person import ChildFactory
from core.models import Person

NUM_USERS = 500


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Person]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            with factory.Faker.override_default_locale("en_GB"):
                person = ChildFactory()
            people.append(person)
