import pandas as pd
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction

from core.validators.csv import check_file, compare_column_headers
from core.validators.importdata import (
    DOMAINS,
    PERSON_FIELDS,
    check_for_blank_data,
    validate_domain,
    validate_person,
)


def check_data_model(df, domain, person_fieldset, domain_fieldset):
    """
    Checks to see if the expected fields are present in the dataframe
    :param df: A dataframe, loaded from CSV likely
    :param domain: The domain of the data being tested (e.g. Education, Police, etc)
    :param person_fieldset: The fields used to store information about a person
    :param domain_fieldset: The fields used to store information about the domain itself
    :return: Returns a True/False value based on if all the required columns are present
    """
    print("These are {} records...".format(domain))
    match_result = compare_column_headers(
        df, list(set(person_fieldset + domain_fieldset))
    )
    return match_result


class Command(BaseCommand):
    help = "Generates test data"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)
        parser.add_argument("service_id", type=int)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        data_file = kwargs["file"]
        # data_target = kwargs["service_id"]  # To be used with matching Later

        try:
            check_file(data_file)
        except ValidationError:
            print("File is empty. Please check and try again")
            return False

        df = pd.read_csv(data_file, sep=",")

        try:
            check_for_blank_data(df)
        except ValidationError:
            print("Found Blank Values in Columns")
            return False

        df, result = validate_person(df)
        if not result:
            print("Required column headers for Person haven't been found")
            return False

        found_domain = False
        for dom in DOMAINS:
            if all(
                x.replace("_", " ").title() in df.columns for x in DOMAINS[dom]["Key"]
            ):
                print("Checking for {}...".format(DOMAINS[dom]["Key"]))
                match_result = check_data_model(
                    df, dom, PERSON_FIELDS, DOMAINS[dom]["Fields"]
                )
                print("Checking domain fields: {}".format(dom))
                df, validation_result = validate_domain(dom, df)
                if not validation_result:
                    print("Records not found to be valid!")
                    return False
                found_domain = True

        if found_domain is False:
            print(
                """Data Structure was unable to be detected. Please refer
                to the schema documentation."""
            )

        if not match_result:
            print("The expected fields were not present")
            return False

        print(df.dtypes)
        print(
            "Data file is Correct"
        )  # Placeholder for now until I can pass to the matching functions.
