import logging

from django.contrib.sessions.models import Session

from core.models import LoggedInUser


class PageViewLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.id if request.user.is_authenticated else "AnonymousUser"
        url = request.path

        logger = logging.getLogger(__name__)
        logger.info(f"User: {user} - URL: {url}")

        response = self.get_response(request)
        return response


class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    # Called once per request
    def __call__(self, request):
        # This codition is required because anonymous users
        # dont have access to 'logged_in_user'
        if request.user.is_authenticated:
            # Gets the user's session_key from the database

            logged_in_user, created = LoggedInUser.objects.get_or_create(
                user=request.user
            )
            current_session_key = logged_in_user.session_key
            # If the session_key exists in the db and it is different from the browser's session
            if (
                current_session_key
                and current_session_key != request.session.session_key
            ):
                if session := Session.objects.filter(
                    session_key=current_session_key
                ).first():
                    session.delete()
            # Update the user's session_key in the db
            logged_in_user.session_key = request.session.session_key
            logged_in_user.save()

        response = self.get_response(request)
        return response
