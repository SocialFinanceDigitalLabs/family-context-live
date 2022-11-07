from faker import Faker

fake = Faker("en_GB")


def get_first_name_from_gender(gender):
    if gender == "M":
        first_name = fake.first_name_male()
    elif gender == "F":
        first_name = fake.first_name_female()
    elif gender == "O":
        first_name = fake.first_name_nonbinary()
    elif gender == "U":
        first_name = fake.first_name()
    else:
        raise ValueError("Input gender must be male, female, or non-binary.")

    return first_name
