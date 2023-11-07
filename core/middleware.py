import logging

logging.basicConfig(filename="user_activity.log", encoding="utf-8", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logging.info("Started logging")

class PageViewLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        url = request.path
        logging.info(f"User: {user} - URL: {url}")
        response = self.get_response(request)
        return response