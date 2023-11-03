from .models import PageViewLog

class PageViewLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        PageViewLog.objects.create(
            user = request.user,
            url = request.path
        )
        response = self.get_response(request)
        return response