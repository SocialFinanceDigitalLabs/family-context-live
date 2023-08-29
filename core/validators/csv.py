import os

import numpy as np
from django.core.exceptions import ValidationError

VALID_IMPORT_EXTENSIONS = [".csv"]


def check_file(data_file):
    """
    Takes a path to a file, and checks to see if it's in the correct format
    :param data_file: String path to file
    """
    file_extension = os.path.splitext(data_file)[1]
    valid_extensions = VALID_IMPORT_EXTENSIONS
    if not file_extension.lower() in valid_extensions:
        msg = "Invalid file, Please use a valid CSV file"
        raise ValidationError("{}".format(msg), status="invalid")


def check_columns(cols, subset):
    """
    Simple function to check to see if a subset is part of a list of columns
    :param cols: The "whole" we're checking against
    :param subset: The potential subset
    :return: True/False depending on if the list is a subset or not
    """
    if set(subset).issubset(set(cols)):
        return True
    return False


def compare_column_headers(df, fields):
    """
    Tests to check if the expected fields are present, and outputs a list
    of missing fields if not
    :param df: Data frame to check.
    :param fields: Required Fields
    :return: True/False based on if the fields were present
    """
    if check_columns(list(df.columns), fields):
        print("All required fields present!")
        return True
    else:
        missing_fields = list(np.setdiff1d(fields, list(df.columns)))
        print(
            "The file doesn't match the expected structure. Missing fields: ",
            missing_fields,
        )
        return False
