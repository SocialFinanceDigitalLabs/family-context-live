import factory
from django.core.management.base import BaseCommand
from django.db import transaction

from core.factories.person import ChildFactory
from core.factories.service import create_services
from core.models import AdultSocialCare, Housing, Person, Police, School, ServiceSummary


class Command(BaseCommand):
    help = "Generates test data"

    def add_arguments(self, parser):
        parser.add_argument("number_of_children", type=int)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        number_of_children = kwargs["number_of_children"]
        self.stdout.write("Deleting old data...")
        models = [Person, Housing, School, AdultSocialCare, Police, ServiceSummary]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # Create the services
        create_services()

        # Create all the users
        people = []
        for _ in range(number_of_children):
            with factory.Faker.override_default_locale("en_GB"):
                person = ChildFactory()
            people.append(person)
