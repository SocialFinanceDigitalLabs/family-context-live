from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from core.middleware import OneSessionPerUserMiddleware
from core.models import LoggedInUser


class OneSessionPerUserMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.middleware = OneSessionPerUserMiddleware(lambda r: r)

    def test_middleware_with_anonymous_user(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        SessionMiddleware(lambda r: r).process_request(request)
        request.session.save()

        self.middleware(request)
        self.assertIsNone(
            LoggedInUser.objects.filter(session_key=request.session.session_key).first()
        )

    def test_middleware_stores_session_key(self):
        user = User.objects.create_user(username="testuser2", password="12345")
        request = self.factory.get("/")
        request.user = user
        SessionMiddleware(lambda r: r).process_request(request)
        request.session.save()

        self.middleware(request)
        self.assertTrue(
            LoggedInUser.objects.filter(
                session_key=request.session.session_key
            ).exists()
        )

    def test_new_session_replaces_old(self):
        # Create first session
        request = self.factory.get("/")
        request.user = self.user
        session_middleware = SessionMiddleware(lambda r: r)
        session_middleware.process_request(request)
        request.session.save()

        # Create second session
        request2 = self.factory.get("/")
        request2.user = self.user
        session_middleware.process_request(request2)
        request2.session.save()

        # Apply middleware
        self.middleware(request2)

        # Test conditions
        self.assertNotEqual(request.session.session_key, request2.session.session_key)
        self.assertFalse(
            LoggedInUser.objects.filter(
                session_key=request.session.session_key
            ).exists()
        )
        self.assertTrue(
            LoggedInUser.objects.filter(
                session_key=request2.session.session_key
            ).exists()
        )
