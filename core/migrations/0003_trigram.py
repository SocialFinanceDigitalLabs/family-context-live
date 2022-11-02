from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_person_address_person_cms_id_person_date_of_birth_and_more"),
    ]

    operations = [
        TrigramExtension(),
    ]
