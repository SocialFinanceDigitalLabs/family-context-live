from django.contrib import admin
from django.urls import include, path, reverse
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from .views import Home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("home/", Home.as_view(), name="home"),
]

if settings.SSO_USED:
    urlpatterns.append(path("accounts/", include("allauth.urls")))
else:
    urlpatterns.append(path("accounts/", include("django.contrib.auth.urls")))
    urlpatterns.append(
        path(
            "account_logout/",
            lambda request: redirect(reverse("logout")),
            name="account_logout",
        )
    )

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
