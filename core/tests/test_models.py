from django.test import TestCase

from core.models import DataSource, Person


class PersonTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(
            first_name="Noah",
            last_name="Smith",
            date_of_birth="2013-11-01",
            age="10",
            nhs_number="1234567890",
        )

    def test_first_name_label(self):
        person = Person.objects.get(id=1)
        self.assertEqual(
            person._meta.get_field("first_name").verbose_name, "first name"
        )

    def test_last_name_label(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person._meta.get_field("last_name").verbose_name, "last name")

    def test_date_of_birth_label(self):
        person = Person.objects.get(id=1)
        self.assertEqual(
            person._meta.get_field("date_of_birth").verbose_name, "date of birth"
        )

    def test_age_label(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person._meta.get_field("age").verbose_name, "age")

    def test_nhs_number_label(self):
        person = Person.objects.get(id=1)
        self.assertEqual(
            person._meta.get_field("nhs_number").verbose_name, "nhs number"
        )


class DataSourceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DataSource.objects.create(name="My Data Source", last_update="2023-09-01")

    def test_last_update_label(self):
        source = DataSource.objects.get(id=1)

        self.assertEqual(
            source._meta.get_field("last_update").verbose_name, "last update"
        )
