import factory
from factory.django import DjangoModelFactory

from core.models import RelationshipType


class ParentRelationshipFactory(DjangoModelFactory):
    class Meta:
        model = "core.PersonRelationship"
        exclude = ("gender_choice",)

    gender_choice = "M"
    relation = factory.SubFactory(
        "core.factories.person.ParentFactory", gender=gender_choice
    )
    relation_type = RelationshipType.PARENT
