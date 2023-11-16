from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Person

User = get_user_model()

class PageViewLoggerTest(TestCase):
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
    
    def test_logs_authenticated_user(self):
        # Login the user
        self.client.login(username="testuser1", password="testpassword123!")

        # Use assertLogs to capture log output during the execution of this block
        with self.assertLogs(logger='core', level='INFO') as log_context:
            # Perform the action that should generate logs
            response = self.client.get("/person/1/")

        # Check that the log message contains the expected information
        expected_log_message = f"User: {response.wsgi_request.user.id} - URL: /person/1/"
        self.assertIn(expected_log_message, log_context.output[0])

    def test_logs_anonymous_user(self):
        with self.assertLogs(logger='core', level='INFO') as log_context:
            response = self.client.get("/person/1/")

        # Check that the log message contains the expected information
        expected_log_message = f"User: AnonymousUser - URL: /person/1/"
        self.assertIn(expected_log_message, log_context.output[0])
