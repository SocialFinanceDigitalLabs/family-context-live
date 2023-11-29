import json
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from core.models import DataSource, Person, Record


class Command(BaseCommand):
    help = "populates the database with data from a csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("files", nargs="+", type=str)

    def update_db(self, file_path, cols_as_expected) -> None:
        data = pd.read_csv(file_path)
        filename = Path(file_path).stem

        # formatting: capitalise first letter.
        filename = filename.title()

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

        # store non-id data as json.
        record_df = data[data.columns.difference(person_cols)]
        json_records = [json.dumps(row) for row in record_df.to_dict("records")]

        datasource, source_created = DataSource.objects.get_or_create(
            name=filename,
            last_update=timezone.now(),
        )
        for ind, row in data.iterrows():
            person, person_created = Person.objects.get_or_create(
                last_name=row["last_name"],
                first_name=row["first_name"],
                date_of_birth=row["date_of_birth"],
                address=row["address"],
                age=row["age"],
                nhs_number=row["nhs_number"],
            )
            Record.objects.create(
                person_id=person,
                datasource_id=datasource,
                record=json_records[ind],
            )

    def handle(self, *args, **kwargs):
        # standardise id column names
        cols_as_expected = {
            "Last Name": "last_name",
            "First Name": "first_name",
            "Date of Birth": "date_of_birth",
            "Address": "address",
            "Age": "age",
            "NHS No": "nhs_number",
        }

        for file in kwargs["files"]:
            self.update_db(file, cols_as_expected)

        self.stdout.write(f"Records: {len(Record.objects.all())}")
        self.stdout.write(f"Persons: {len(Person.objects.all())}")
        self.stdout.write(str(DataSource.objects.all()))
        self.stdout.write(self.style.SUCCESS("Database updated successfully"))
