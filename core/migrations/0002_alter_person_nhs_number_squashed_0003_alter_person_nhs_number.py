# Generated by Django 4.2.7 on 2023-11-17 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("core", "0002_alter_person_nhs_number"),
        ("core", "0003_alter_person_nhs_number"),
    ]

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="nhs_number",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
