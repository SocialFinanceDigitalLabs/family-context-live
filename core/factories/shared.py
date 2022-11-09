from faker import Faker

from core.models import Gender

fake = Faker("en_GB")


def get_first_name_from_gender(gender):
    if gender == Gender.MALE:
        first_name = fake.first_name_male()
    elif gender == Gender.FEMALE:
        first_name = fake.first_name_female()
    elif gender == Gender.OTHER:
        first_name = fake.first_name_nonbinary()
    elif gender == Gender.NOT_SPECIFIED:
        first_name = fake.first_name()
    else:
        raise ValueError("Input gender must be male, female, or non-binary.")

    return first_name
