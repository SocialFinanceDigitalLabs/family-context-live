import factory
from factory.django import DjangoModelFactory

from core.models import Gender, RelationshipType


class ParentRelationshipFactory(DjangoModelFactory):
    class Meta:
        model = "core.PersonRelationship"
        exclude = ("gender_choice", "specified_last_name", "specified_address")

    # Fields that may need to be shared between people in a relation,
    # along with defaults if not shared
    gender_choice = Gender.MALE
    specified_last_name = factory.Faker("last_name")
    specified_address = factory.Faker("address")

    # Model fields
    relation = factory.SubFactory(
        "core.factories.person.ParentFactory",
        gender=gender_choice,
        last_name=specified_last_name,
        address=specified_address,
    )
    relation_type = RelationshipType.PARENT
