import random
from datetime import datetime
from random import randint

import factory.fuzzy
from dateutil.relativedelta import relativedelta
from factory.django import DjangoModelFactory

from core.models import ServiceInvolvement


class HousingFactory(DjangoModelFactory):
    service_involvement = factory.LazyAttribute(
        lambda o: random.choices(ServiceInvolvement.choices)[0][0]
    )
    housing_association = factory.Faker("company")
    contact = factory.SubFactory("core.factories.contact.ContactFactory")
    tenancy_start = factory.fuzzy.FuzzyDate(
        datetime.now() - relativedelta(years=randint(1, 3)), datetime.now()
    )
    antisocial_behaviour = factory.LazyAttribute(
        lambda o: random.choices([True, False], cum_weights=(5, 95), k=1)[0]
    )
    rent_arrears = factory.LazyAttribute(
        lambda o: random.choices([True, False], cum_weights=(5, 95), k=1)[0]
    )
    notice_seeking_possession = factory.LazyAttribute(
        lambda o: random.choices([True, False], cum_weights=(5, 95), k=1)[0]
    )
    eviction = factory.LazyAttribute(
        lambda o: random.choices([True, False], cum_weights=(5, 95), k=1)[0]
    )
    start_date_of_last_involvement = datetime(2020, 1, 1)
    date_of_most_recent_interaction = datetime(2022, 1, 1)
    date_current_as_of = datetime(2022, 10, 1)
    coverage_start_date = datetime(2019, 1, 1)
    coverage_end_date = datetime(2022, 11, 1)
    coverage_geographic_area = " "
    other = {}

    class Meta:
        model = "core.Housing"
