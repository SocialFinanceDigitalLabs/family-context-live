import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from core.forms import NameSearchForm, NHSIdForm
from core.models import DataSource, Person, Record
from core.search import person_search


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "home.html")


def login(request):
    return render(request, "registration/login.html")


@login_required()
def search(request):
    name_form = NameSearchForm()
    nhs_form = NHSIdForm()
    return render(
        request,
        "search.html",
        {"name_form": name_form, "sub": "search", "nhs_form": nhs_form},
    )


@login_required()
def name_search(request):
    if request.method == "POST":
        form = NameSearchForm(request.POST)
        if form.is_valid():
            date_of_birth: datetime.date = form.cleaned_data["date_of_birth"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            results = person_search(first_name, last_name, date_of_birth)

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

    return render(request, "name_search.html", {"form": form, "sub": "name_search"})


@login_required()
def nhs_id_search(request):
    if request.method == "POST":
        form = NHSIdForm(request.POST)
        if form.is_valid():
            nhs_number = form.cleaned_data["nhs_number"]
            results = Person.objects.filter(Q(nhs_number__icontains=nhs_number))
            if not results:
                # Need to display error that record wasn't found...
                return render(
                    request,
                    "search_results.html",
                    {
                        "results": results,
                        "terms": nhs_number,
                    },
                )
            elif len(results) == 1:
                return redirect(reverse("person", kwargs={"person_id": results[0].id}))
            else:
                return render(
                    request,
                    "search_results.html",
                    {"results": results, "terms": form.cleaned_data["nhs_number"]},
                )
    else:
        nhs_form = NHSIdForm()
        name_form = NameSearchForm()

    return render(
        request,
        "search.html",
        {"name_form": name_form, "sub": "search", "nhs_form": nhs_form},
    )


@login_required()
def person(request, person_id):
    p = Person.objects.get(id=person_id)
    data_sources = DataSource.objects.all()

    # runtime attribute to indicate if service contains data about person.
    for source in data_sources:
        source.person_record = Record.objects.filter(person_id=person_id).filter(
            datasource_id=source.id
        )
        source.contains_person = source.person_record.exists()

    return render(
        request,
        "person.html",
        {
            "person": p,
            "data_sources": data_sources,
        },
    )


@login_required()
def get_service_records(request, person_id, datasource_id):
    person = Person.objects.get(id=person_id)
    data_source = DataSource.objects.get(id=datasource_id)

    # get service records for person as list[dict]
    json_person_records = Record.objects.filter(person_id=person_id).filter(
        datasource_id=datasource_id
    )
    data_source.person_records = [
        json.loads(record.record) for record in json_person_records
    ]

    return render(
        request,
        "person_service_records.html",
        {"person": person, "data_source": data_source, "sub": "get_service_records"},
    )
