import csv
import os
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
import yaml
import uuid
from faker import Faker

fake = Faker("en_GB")
BASE_FIXTURES_DIR = "./fixtures"


class Person:
    """
    A person is someone who has data in Family Context. They have common attributes specified here that are used for matching.
    All other fields are per-data-source specified in the YAML files specified in the fixtures directory
    """

    def __init__(self):
        # Standard fields that will exist across all data sets
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.date_of_birth = fake.date_of_birth(
            tzinfo=None, minimum_age=18, maximum_age=85
        )
        self.age = self.calculate_age_from_dob()
        self.nhs_no = str(uuid.uuid4().int)[:10]
        self.address = fake.address().replace("\n", " ")

    def calculate_age_from_dob(self):
        """
        Calculate a valid age given a date of birth
        """
        current_date = datetime.now()
        return (
            current_date.year
            - self.date_of_birth.year
            - (
                (current_date.month, current_date.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )


def generate_fake_value(data_type):
    """
    Matches up the specified data types specified by the LA to
    """
    if data_type == "FullName":
        return f"{fake.first_name()} {fake.last_name()}"
    elif data_type == "Name":
        return fake.first_name()
    elif data_type == "Surname":
        return fake.last_name()
    elif data_type == "Company":
        return fake.company()
    elif data_type == "String":
        return "Lorem ipsum dolor sit amet"
    elif data_type == "Date":
        return fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65)
    elif data_type == "RecentDate":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        return fake.date_between_dates(date_start=start_date, date_end=end_date)
    elif data_type == "Numeric":
        return random.randint(0, 100)
    elif data_type == "Boolean":
        return random.choice(["Yes", "No"])
    elif data_type == "Email":
        return fake.email()


class Command(BaseCommand):
    help = "Generates a dummy CSV file with random data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--people",
            type=int,
            help="The number of people to generate",
            required=False,
            default=100,
        )
        parser.add_argument(
            "--chance",
            type=int,
            default=90,
            required=False,
            help="The percent chance a generated person will appear in any given data source",
        )
        parser.add_argument(
            "--la",
            type=str,
            required=False,
            default="hounslow",
            choices=["hounslow", "brent"],
            help="LA to generate data for",
        )

    def handle(self, *args, **options):
        person_count = options["people"]
        data_set_appearance_chance = options["chance"]
        la = options["la"]

        # Perform manual validation for minimum and maximum values
        if data_set_appearance_chance is not None and (
            data_set_appearance_chance < 1 or data_set_appearance_chance > 100
        ):
            self.stderr.write(
                "Error: The percent chance speicified is outside the valid range (1 to 100)."
            )
            return

        common_fields, data_sets = self.load_fixture_structure(la)
        if not common_fields and not data_sets:
            return

        # First, delete existing data sets
        self.clear_fixtures_folder()

        # Second, loop over the number of people expected to generate
        for _ in range(person_count):
            p = Person()

            # Next, pick which data sets that person exists in...
            for data_set in data_sets:

                # Assemble headers for this data set
                fieldnames = common_fields.copy()
                fieldnames.extend(list(data_set["fields"].keys()))

                # We don't necessarily want every person to exist in every data set...
                if random.randint(1, 100) <= data_set_appearance_chance:
                    output_file = os.path.join(
                        BASE_FIXTURES_DIR, data_set["_Data_type"]
                    )

                    if not os.path.exists(output_file):
                        # If this is the first time the file is being written to...
                        with open(output_file, "a", newline="\n") as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            self.write_data(data_set, writer, p)
                    else:
                        # An already existing file...
                        with open(output_file, "a", newline="\n") as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            self.write_data(data_set, writer, p)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully generated data for {p.first_name} {p.last_name}"
                )
            )

    def load_fixture_structure(self, la):
        """
        Handles loading the data structure specified by a given LA
        from the YAML files located in the fixtures structures directory
        """
        structure_file_path = os.path.join(
            BASE_FIXTURES_DIR, "structures", f"{la}_data.yaml"
        )
        try:
            with open(structure_file_path, "r") as structure_file:
                structure_data = yaml.safe_load(structure_file)
            common_fields = structure_data["COMMON_FIELD_NAMES"]
            data_sets = structure_data["DataTypes"]
        except FileNotFoundError as err:
            self.stderr.write(
                f"Problem opening the YAML structure file {structure_file_path}: {err}"
            )
            return None, None
        except yaml.YAMLError as err:
            self.stderr.write(f"Problem parsing YAML file: {err}")
            return None, None

        return common_fields, data_sets

    def write_data(self, data_set, writer, person):
        """
        Creates the CSV row to be written given the data (some saved, some generated randomly new)
        """

        data = {
            "First Name": person.first_name,
            "Last Name": person.last_name,
            "Date of Birth": person.date_of_birth,
            "Age": person.age,
            "NHS No": person.nhs_no,
            "Address": person.address,
        }

        for field, data_type in data_set["fields"].items():
            data[field] = generate_fake_value(data_type)

        writer.writerow(data)

    def clear_fixtures_folder(self):
        """
        Clear all CSV files in the fixtures directory
        """
        try:
            for filename in os.listdir(BASE_FIXTURES_DIR):
                if filename.endswith(".csv"):
                    file_path = os.path.join(BASE_FIXTURES_DIR, filename)
                    os.remove(file_path)
        except OSError as err:
            self.stderr.write(f"Error: {err}")
