from collections import OrderedDict
from datetime import datetime
from random import randint

import factory
import factory.fuzzy
from dateutil.relativedelta import relativedelta
from factory.django import DjangoModelFactory

from core.models import Gender, Person, RelationshipType

from .housing import HousingFactory
from .relationship import ParentRelationshipFactory
from .school import SchoolFactory
from .shared import age_from_birth_date, get_first_name_from_gender


class ParentFactory(DjangoModelFactory):

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
    last_name = factory.Faker("last_name")
    address = factory.Faker("address")

    cms_id = randint(1000000, 99999999)
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.now() - relativedelta(years=55),
        datetime.now() - relativedelta(years=32),
    )

    first_name = factory.LazyAttribute(lambda o: get_first_name_from_gender(o.gender))

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
        relation_type=RelationshipType.PARENT,
        passed_gender=Gender.FEMALE,
        passed_last_name=factory.SelfAttribute("..last_name"),
        passed_address=factory.SelfAttribute("..address"),
    )

    dad = factory.RelatedFactory(
        ParentRelationshipFactory,
        factory_related_name="person",
        relation_type=RelationshipType.PARENT,
        passed_gender=Gender.MALE,
        passed_last_name=factory.SelfAttribute("..last_name"),
        passed_address=factory.SelfAttribute("..address"),
    )

    # Only makes sense for a child to be in school if they're older than 6...
    school = factory.Maybe(
        factory.LazyAttribute(lambda o: age_from_birth_date(o.date_of_birth) > 6),
        factory.RelatedFactoryList(SchoolFactory, "person", size=lambda: randint(1, 3)),
    )

    class Meta:
        model = Person
