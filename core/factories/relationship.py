import factory
from factory.django import DjangoModelFactory

from core.models import RelationshipType


class ParentRelationshipFactory(DjangoModelFactory):
    class Meta:
        model = "core.PersonRelationship"
        exclude = ("passed_last_name", "passed_gender", "passed_address")

    class Params:
        passed_last_name = ""
        passed_address = ""
        passed_gender = ""

    # Fields that may need to be shared between people in a relation,
    # along with defaults if not shared

    # Model fields
    relation = factory.SubFactory(
        "core.factories.person.ParentFactory",
        last_name=factory.SelfAttribute("..passed_last_name"),
        gender=factory.SelfAttribute("..passed_gender"),
        address=factory.SelfAttribute("..passed_address"),
    )
    relation_type = RelationshipType.PARENT
