import itertools
import random
import string
from typing import Optional

from django.contrib.auth.models import User
from faker import Faker

from core.models import Person


class Builder:
    """build fake data, for tests or local setup"""

    def __init__(self, seed: Optional[int] = None):
        if seed:
            Faker.seed(seed)
        self.fake = Faker("en-GB")
        self._user_count = itertools.count()

    def user(self, faker=True, **kwargs) -> User:
        """
        Create a user. Pass 'faker=False' to use test-friendly values
        """
        user_count = next(self._user_count)

        default_props = dict(password="test")
        if faker:
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            default_props["first_name"] = first_name
            default_props["last_name"] = last_name
            email = f"{first_name.lower()}.{last_name.lower()}{''.join(random.choices(string.ascii_lowercase, k=4))}@example.test"
        else:
            default_props["first_name"] = f"FirstName{user_count}"
            default_props["last_name"] = f"LastName{user_count}"
            email = f"user{user_count}@example.test"

        default_props["email"] = email
        default_props["username"] = email
        default_props.update(kwargs)

        user = User.objects.create_user(**default_props)

        return user

    def person(
        self,
        last_name=None,
        first_name=None,
        date_of_birth=None,
        address=None,
        age=None,
        nhs_number=None,
        **kwargs,
    ) -> Person:
        person = Person.objects.create(
            last_name=last_name or self.fake.last_name(),
            first_name=first_name or self.fake.first_name(),
            date_of_birth=date_of_birth or self.fake.date_of_birth(),
            address=address or self.fake.address(),
            age=age or self.fake.pyint(min_value=18, max_value=85),
            nhs_number=nhs_number or self.fake.bothify(text="### ### ####", letters=""),
            **kwargs,
        )

        return person
