from collections import OrderedDict
from datetime import datetime
from random import randint

import factory
import factory.fuzzy
from dateutil.relativedelta import relativedelta
from factory.django import DjangoModelFactory

from .shared import get_first_name_from_gender


class ParentFactory(DjangoModelFactory):
    cms_id = randint(1000000, 99999999)
    gender = factory.Faker(
        "random_element",
        elements=OrderedDict([("M", 0.47), ("F", 0.47), ("O", 0.03), ("U", 0.03)]),
    )
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.now() - relativedelta(years=randint(32, 55)), datetime.now()
    )

    first_name = factory.LazyAttribute(lambda o: get_first_name_from_gender(o.gender))
    last_name = factory.Faker("last_name")

    address = factory.Faker("address")

    housing = factory.RelatedFactoryList(
        "core.factories.housing.HousingFactory", "person", size=lambda: randint(1, 3)
    )

    class Meta:
        model = "core.Person"


class ChildFactory(DjangoModelFactory):
    cms_id = randint(1000000, 99999999)
    first_name = factory.LazyAttribute(lambda o: get_first_name_from_gender(o.gender))
    last_name = factory.Faker("last_name")
    address = factory.Faker("address")
    gender = factory.Faker(
        "random_element",
        elements=OrderedDict([("M", 0.47), ("F", 0.47), ("O", 0.03), ("U", 0.03)]),
    )
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.now() - relativedelta(years=randint(1, 16)), datetime.now()
    )

    school = factory.RelatedFactoryList(
        "core.factories.school.SchoolFactory", "person", size=lambda: randint(1, 3)
    )

    mum = factory.RelatedFactory(
        "core.factories.relationship.ParentRelationshipFactory",
        "person",
        gender_choice="F",
    )
    dad = factory.RelatedFactory(
        "core.factories.relationship.ParentRelationshipFactory",
        "person",
        gender_choice="M",
    )

    class Meta:
        model = "core.Person"
