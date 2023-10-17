import pandas as pd
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from core.models import Person, DataSource, Record


class Command(BaseCommand):
    help = "populates the database with data from a csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("files", nargs="+", type=str)

    def update_db(self, file) -> None:
        data = pd.read_csv(file)
        filename = file.split("\\")[-1].split(".")[0]

        # standardise id column names
        cols_as_expected = {
            "Last Name": "last_name",
            "First Name": "first_name",
            "Date of Birth": "date_of_birth",
            "Address": "address",
            "Age": "age",
            "NHS No": "nhs_number",
        }
        data.rename(columns=cols_as_expected, inplace=True)

        # separate record data from person data
        person_cols = [
            "last_name",
            "first_name",
            "date_of_birth",
            "address",
            "age",
            "nhs_number",
        ]
        json_records = data[data.columns.difference(person_cols)].to_json(
            orient="records"
        )

        datasource = DataSource.objects.create(
            name=filename,
            last_update=timezone.now(),
        )
        for ind, row in data.iterrows():
            person = Person.objects.create(
                last_name=row["last_name"],
                first_name=row["first_name"],
                date_of_birth=row["date_of_birth"],
                address=row["address"],
                age=row["age"],
                nhs_number=row["nhs_number"],
            )
            record = Record.objects.create(
                person_id=person,
                datasource_id=datasource,
                record=json_records[ind],
            )

    def handle(self, *args, **kwargs):
        Record.objects.all().delete()
        DataSource.objects.all().delete()
        Person.objects.all().delete()

        for file in kwargs["files"]:
            self.update_db(file)
        
        self.stdout.write(f"Records: {len(Record.objects.all())}")
        self.stdout.write(f"Persons: {len(Person.objects.all())}")
        self.stdout.write(str(DataSource.objects.all()))
        self.stdout.write(self.style.SUCCESS("Database updated successfully"))
