import logging

class PageViewLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        url = request.path

        logger =  logging.getLogger(__name__)
        logger.info(f"User: {user} - URL: {url}")

        response = self.get_response(request)
        return response