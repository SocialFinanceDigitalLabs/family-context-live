import random
from datetime import datetime

import factory
from factory.django import DjangoModelFactory

from core.models import ServiceInvolvement


class SchoolFactory(DjangoModelFactory):
    name_prefix = factory.Faker("company")
    service_involvement = factory.LazyAttribute(
        lambda o: random.choices(ServiceInvolvement.choices)[0][0]
    )
    school_name = factory.LazyAttribute(
        lambda o: "{} School".format(o.name_prefix.split(" ")[0])
    )
    contact_number = factory.Faker("phone_number")
    admission_type = "test"
    coverage_geographic_area = "test"
    start_date_of_last_involvement = datetime(2020, 1, 1)
    date_of_most_recent_interaction = datetime(2022, 1, 1)
    date_current_as_of = datetime(2022, 10, 1)
    coverage_start_date = datetime(2019, 1, 1)
    coverage_end_date = datetime(2022, 11, 1)

    class Meta:
        model = "core.School"
        exclude = "name_prefix"
