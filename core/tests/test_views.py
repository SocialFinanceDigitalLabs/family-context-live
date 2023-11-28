from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import DataSource, Person, Record

User = get_user_model()


class SearchPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username="testuser1", password="testpassword123!"
        )
        test_user1.save()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser1", password="testpassword123!")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class PersonPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username="testuser1", password="testpassword123!"
        )
        test_user1.save()

        Person.objects.create(
            first_name="Olivia",
            last_name="Jones",
            date_of_birth="2013-11-01",
            age="10",
            nhs_number="1234567890",
        )

    def test_person_restricted_access(self):
        response = self.client.get("/person/1/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser1", password="testpassword123!")
        response = self.client.get("/person/1/")
        self.assertEqual(response.status_code, 200)


class DataSourcePersonPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username="testuser1", password="testpassword123!"
        )
        test_user1.save()

        person = Person.objects.get_or_create(
            first_name="Olivia",
            last_name="Jones",
            date_of_birth="2013-11-01",
            age="10",
            nhs_number="1234567890",
        )[0]

        source = DataSource.objects.get_or_create(
            name="My Data Source", last_update="2023-09-01"
        )[0]

        Record.objects.create(
            person_id=person, datasource_id=source, record='{"some":"field"}'
        )

    def test_record_restricted_access(self):
        response = self.client.get("/person/1/service/1/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser1", password="testpassword123!")
        response = self.client.get("/person/1/service/1/")
        self.assertEqual(response.status_code, 200)
