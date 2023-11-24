from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.builder import Builder
from core.search import person_search

User = get_user_model()


class PersonSearchTest(TestCase):
    builder = Builder()

    def setUp(self) -> None:
        super().setUp()
        self.john_smith = self.builder.person(
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1950, 1, 1),
        )
        self.john_superman = self.builder.person(
            first_name="John",
            last_name="Superman",
            date_of_birth=date(1960, 1, 1),
        )
        self.john_cheese = self.builder.person(
            first_name="John",
            last_name="Cheese",
            date_of_birth=date(1970, 1, 1),
        )
        self.jane_smith = self.builder.person(
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1980, 1, 1),
        )
        self.jane_cheese = self.builder.person(
            first_name="Jane",
            last_name="Cheese",
            date_of_birth=date(1990, 1, 1),
        )

    def test_search_first_and_last_name(self):
        results = person_search(
            first_name="John",
            last_name="Smith",
        )
        first_person = list(results)[0]
        last_person = list(results)[-1]
        self.assertEqual(len(results), 4)
        self.assertEqual(first_person, self.john_smith)
        self.assertEqual(last_person, self.jane_smith)

    def test_search_first_letter_of_last_name(self):
        results = person_search(first_name="John", last_name="S")
        first_person = list(results)[0]
        last_person = list(results)[-1]
        self.assertEqual(len(results), 5)
        self.assertEqual(first_person, self.john_smith)
        self.assertEqual(last_person, self.jane_cheese)

    def test_search_date_of_birth(self):
        results = person_search(
            first_name="John",
            last_name="S",
            date_of_birth=date(1960, 1, 1),
        )
        first_person = list(results)[0]
        last_person = list(results)[-1]
        self.assertEqual(len(results), 5)
        self.assertEqual(first_person, self.john_superman)
        self.assertEqual(last_person, self.jane_cheese)
