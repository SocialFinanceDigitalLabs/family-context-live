from collections import OrderedDict
from datetime import datetime
from random import randint

import factory
import factory.fuzzy
from dateutil.relativedelta import relativedelta
from factory.django import DjangoModelFactory

from core.models import Gender, Person

from .housing import HousingFactory
from .relationship import ParentRelationshipFactory
from .school import SchoolFactory
from .shared import get_first_name_from_gender


class ParentFactory(DjangoModelFactory):
    cms_id = randint(1000000, 99999999)
    gender = factory.Faker(
        "random_element",
        elements=OrderedDict(
            [
                (Gender.MALE, 0.47),
                (Gender.FEMALE, 0.47),
                (Gender.OTHER, 0.03),
                (Gender.NOT_SPECIFIED, 0.03),
            ]
        ),
    )
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.now() - relativedelta(years=randint(32, 55)), datetime.now()
    )

    first_name = factory.LazyAttribute(lambda o: get_first_name_from_gender(o.gender))
    last_name = factory.Faker("last_name")

    address = factory.Faker("address")

    housing = factory.RelatedFactoryList(
        HousingFactory, "person", size=lambda: randint(1, 3)
    )

    class Meta:
        model = Person


class ChildFactory(DjangoModelFactory):
    cms_id = randint(1000000, 99999999)
    first_name = factory.LazyAttribute(lambda o: get_first_name_from_gender(o.gender))
    last_name = factory.Faker("last_name")
    address = factory.Faker("address")
    gender = factory.Faker(
        "random_element",
        elements=OrderedDict(
            [
                (Gender.MALE, 0.47),
                (Gender.FEMALE, 0.47),
                (Gender.OTHER, 0.03),
                (Gender.NOT_SPECIFIED, 0.03),
            ]
        ),
    )
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.now() - relativedelta(years=randint(1, 16)), datetime.now()
    )

    school = factory.RelatedFactoryList(
        SchoolFactory, "person", size=lambda: randint(1, 3)
    )

    mum = factory.RelatedFactory(
        ParentRelationshipFactory,
        factory_related_name="person",
        gender_choice=Gender.FEMALE,
        specified_last_name=factory.SelfAttribute("..last_name"),
        specified_address=factory.SelfAttribute("..address"),
    )

    dad = factory.RelatedFactory(
        ParentRelationshipFactory,
        factory_related_name="person",
        gender_choice=Gender.MALE,
        specified_last_name=factory.SelfAttribute("..last_name"),
        specified_address=factory.SelfAttribute("..address"),
    )

    class Meta:
        model = Person
