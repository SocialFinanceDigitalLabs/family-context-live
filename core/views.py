from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import CmsIdForm, NameSearchForm
from .helpers.shared import find_service_involvement_count
from .models import Person, ServiceSummary


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "home.html")


def login(request):
    return render(request, "registration/login.html")


@login_required()
def search(request):
    name_form = NameSearchForm()
    cms_form = CmsIdForm()
    return render(
        request,
        "search.html",
        {"name_form": name_form, "sub": "search", "cms_form": cms_form},
    )

    return render(request, "search.html")


@login_required()
def name_search(request):
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

    return render(request, "name_search.html", {"form": form, "sub": "name_search"})


@login_required()
def case_id_search(request):
    if request.method == "POST":
        form = CmsIdForm(request.POST)
        if form.is_valid():
            cms_id = form.cleaned_data["cms_id"]
            results = Person.objects.filter(cms_id=cms_id)

            if not results:
                # Need to display error that record wasn't found...
                form = CmsIdForm()
            elif len(results) == 1:
                return redirect(reverse("person", kwargs={"person_id": results[0].id}))
            else:
                return render(
                    request,
                    "search_results.html",
                    {"results": results, "terms": form.cleaned_data["cms_id"]},
                )
    else:
        form = CmsIdForm()

    return render(request, "search.html", {"form": form, "sub": "case_id_search"})


@login_required()
def person(request, person_id):
    p = Person.objects.get(id=person_id)
    relation_count = len(p.relationships.all()) + len(p.reverse_relationships.all())
    s = ServiceSummary.objects.all()
    for service in s:
        service.records = find_service_involvement_count(service, p)

    return render(
        request,
        "person.html",
        {"person": p, "relation_count": relation_count, "service_list": s},
    )


@login_required()
def get_service_records(request, person_id, service_id):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if is_ajax:
        if request.method == "GET":
            service_record = ServiceSummary.objects.get(id=service_id)
            person = Person.objects.filter(id=person_id).first()

            records = [
                service_record.service_adult_social_care_records.filter(
                    person=person
                ).values(
                    "local_authority_organisation",
                    "contact",
                    "service_involvement",
                    "start_date_of_last_involvement",
                    "date_of_most_recent_interaction",
                    "date_current_as_of",
                    "coverage_start_date",
                    "coverage_end_date",
                    "coverage_geographic_area",
                    "other",
                ),
                service_record.service_school_records.filter(person=person).values(
                    "school_name",
                    "contact_number",
                    "admission_type",
                    "service_involvement",
                    "start_date_of_last_involvement",
                    "date_of_most_recent_interaction",
                    "date_current_as_of",
                    "coverage_start_date",
                    "coverage_end_date",
                    "coverage_geographic_area",
                    "other",
                ),
                service_record.service_housing_records.filter(person=person).values(
                    "housing_association",
                    "contact",
                    "tenancy_start",
                    "antisocial_behaviour",
                    "rent_arrears",
                    "notice_seeking_possession",
                    "eviction",
                    "service_involvement",
                    "start_date_of_last_involvement",
                    "date_of_most_recent_interaction",
                    "date_current_as_of",
                    "coverage_start_date",
                    "coverage_end_date",
                    "coverage_geographic_area",
                    "other",
                ),
                service_record.service_police_records.filter(person=person).values(
                    "police_area", "contact", "other"
                ),
            ]

            html = render_to_string(
                "person_service_records.html",
                {"service": service_record, "records": records},
            )
            html = html.replace("\n", "").replace('"', "")
            return JsonResponse(html, safe=False)
        else:
            return JsonResponse({"status": "Invalid request"}, status=400)

    else:
        return HttpResponseBadRequest("Invalid request")
