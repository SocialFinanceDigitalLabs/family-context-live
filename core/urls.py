from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search", views.search, name="name_search"),
    path("case_id_search", views.case_id_search, name="case_id_search"),
    path("person", views.person, name="person"),
]
