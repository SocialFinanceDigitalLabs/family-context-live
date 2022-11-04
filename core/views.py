from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CmsIdForm, NameSearchForm
from .models import Person


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "home.html")


def login(request):
    return render(request, "registration/login.html")


@login_required()
def search(request):
    if request.method == "POST":
        form = NameSearchForm(request.POST)
        if form.is_valid():
            dob = form.cleaned_data["date_of_birth"]
            if not dob:
                results = (
                    Person.objects.annotate(
                        similarity=TrigramSimilarity(
                            "first_name", form.cleaned_data["first_name"]
                        )
                        + TrigramSimilarity("last_name", form.cleaned_data["last_name"])
                    )
                    .filter(similarity__gt=0.5)
                    .order_by("-similarity")
                )
            else:
                results = (
                    Person.objects.annotate(
                        similarity=TrigramSimilarity(
                            "first_name", form.cleaned_data["first_name"]
                        )
                        + TrigramSimilarity("last_name", form.cleaned_data["last_name"])
                    )
                    .filter(Q(similarity__gt=0.5) & Q(date_of_birth=dob))
                    .order_by("-similarity")
                )

            return render(
                request,
                "search_results.html",
                {
                    "results": results,
                    "terms": form.cleaned_data["first_name"]
                    + " "
                    + form.cleaned_data["last_name"],
                },
            )
    else:
        form = NameSearchForm()

    return render(request, "search.html", {"form": form, "sub": "name_search"})


@login_required()
def case_id_search(request):
    if request.method == "POST":
        form = CmsIdForm(request.POST)
        if form.is_valid():
            cms_id = form.cleaned_data["cms_id"]
            results = Person.objects.filter(cms_id=cms_id)

            return render(
                request,
                "search_results.html",
                {"results": results, "terms": form.cleaned_data["cms_id"]},
            )
    else:
        form = CmsIdForm()

    return render(request, "search.html", {"form": form, "sub": "case_id_search"})


@login_required()
def person(request):
    return render(request, "person.html")
