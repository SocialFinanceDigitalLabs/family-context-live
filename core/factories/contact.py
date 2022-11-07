import factory
from factory.django import DjangoModelFactory


class ContactFactory(DjangoModelFactory):
    name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    role = " "
    other = {}

    class Meta:
        model = "core.Contact"
