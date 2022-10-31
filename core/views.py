from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, "home.html")


def login(request):
    return render(request, "registration/login.html")


@login_required()
def search(request):
    return render(request, "search.html")


@login_required()
def person(request):
    return render(request, "person.html")
