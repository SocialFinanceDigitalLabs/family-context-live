from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import NHSIdForm, NameSearchForm
from .models import Person, DataSource, Record

import json
from fuzzywuzzy import fuzz

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
            # threshold value (0-100) is directly proportional to similarity between search terms and results
            threshold = 50
            persons = Person.objects.all()
            results = [person for person in persons if (fuzz.ratio(person.first_name, form.cleaned_data["first_name"]) > threshold) | (fuzz.ratio(person.last_name, form.cleaned_data["last_name"]) > threshold)]

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
def case_id_search(request):
    if request.method == "POST":
        form = NHSIdForm(request.POST)
        if form.is_valid():
            nhs_number = form.cleaned_data["nhs_number"]
            results = Person.objects.filter(nhs_number=nhs_number)

            if not results:
                # Need to display error that record wasn't found...
                form = NHSIdForm()
            elif len(results) == 1:
                return redirect(reverse("person", kwargs={"person_id": results[0].id}))
            else:
                return render(
                    request,
                    "search_results.html",
                    {"results": results, "terms": form.cleaned_data["nhs_number"]},
                )
    else:
        form = NHSIdForm()

    return render(request, "search.html", {"form": form, "sub": "case_id_search"})


@login_required()
def person(request, person_id):
    p = Person.objects.get(id=person_id)
    data_sources = DataSource.objects.all()

    # runtime attribute to indicate if service contains data about person.
    for source in data_sources:
        source.person_record = Record.objects.filter(person_id=person_id).filter(datasource_id=source.id)
        source.contains_person = source.person_record.exists()
    

    return render(
        request,
        "person.html",
        {"person": p, "data_sources": data_sources,},
    )


@login_required()
def get_service_records(request, person_id, datasource_id):

    person = Person.objects.get(id=person_id)
    data_source = DataSource.objects.get(id=datasource_id)

    # get service records for person as list[dict]
    json_person_records = Record.objects.filter(person_id=person_id).filter(datasource_id=datasource_id)
    data_source.person_records = [json.loads(record.record) for record in json_person_records]

    return render(request, "person_service_records.html", {"person":person, "data_source": data_source, "sub": "get_service_records"})