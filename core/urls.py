from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search", views.index, name="search"),
    path("person", views.index, name="person"),
]
