from django.urls import path

from core import views

urlpatterns = [
    path("", views.search, name="home"),
    path("search", views.search, name="search"),
    path("search_name", views.name_search, name="name_search"),
    path("nhs_id_search", views.nhs_id_search, name="nhs_id_search"),
    path("person/<int:person_id>/", views.person, name="person"),
    path(
        "person/<int:person_id>/service/<int:datasource_id>/",
        views.get_service_records,
        name="get_service_records",
    ),
]
