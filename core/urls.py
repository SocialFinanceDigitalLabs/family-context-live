from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search", views.search, name="search"),
    path("person", views.person, name="person"),
]
