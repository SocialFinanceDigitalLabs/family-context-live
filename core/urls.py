from django.urls import path

from core import views

urlpatterns = [
    path("", views.search, name="home"),
    path("search", views.search, name="search"),
    path("search_name", views.name_search, name="name_search"),
    path("case_id_search", views.case_id_search, name="case_id_search"),
    path("person/<int:person_id>/", views.person, name="person"),
]
