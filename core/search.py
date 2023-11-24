import datetime
from functools import reduce
from operator import add
from typing import Any, Optional

from django.db.models import Case, F, IntegerField, Q, QuerySet, Value, When

from core.models import Person


def person_search(
    first_name: str, last_name: str, date_of_birth: Optional[datetime.date] = None
) -> QuerySet[Person]:
    """
    Filter people based on their first name, last name, and optional date of birth.
    Rank them by corresponding match relevance.

        Args:
        first_name (str): The first name of the person to search for.
        last_name (str): The last name of the person to search for.
        date_of_birth (Optional[datetime.date], optional): The date of birth of the person to search for. Defaults to None.

    Returns:
        QuerySet[Person]: The queryset of persons matching the search criteria, ordered by a matching rank.

    """
    query = Q(first_name__icontains=first_name) | Q(last_name__icontains=last_name)
    if date_of_birth is not None:
        query = query | Q(date_of_birth=date_of_birth)

    # apply base filtering
    results = Person.objects.filter(query)

    annotations = dict(
        k10=score_annotation("first_name", "iexact", first_name, 4),
        k20=score_annotation("last_name", "iexact", last_name, 4),
        k30=score_annotation("first_name", "istartswith", first_name, 2),
        k40=score_annotation("last_name", "istartswith", last_name, 2),
    )
    if date_of_birth is not None:
        dob_annotations = dict(
            k60=score_annotation("date_of_birth", "year", date_of_birth.year, 1),
            k70=score_annotation("date_of_birth", "month", date_of_birth.month, 1),
            k80=score_annotation("date_of_birth", "day", date_of_birth.day, 1),
        )
        annotations.update(dob_annotations)

    # sum all the score annotation values
    annotations["rank"] = reduce(add, (F(key) for key in annotations.keys()))

    # sort by rank
    results = results.annotate(**annotations).order_by("-rank")
    return results


def score_annotation(
    field_name: str, expression: Optional[str], value: Any, score: int
) -> Case:
    """
    Calculate the score for an annotation based on the field name, expression, value, and score.

    Args:
        field_name (str): The name of the field.
        expression (Optional[str]): The expression to apply to the field (e.g., "gt", "lt", "exact", "year").
        value (Any): The value to compare against the field.
        score (float): The resulting score for the annotation.

    Returns:
        Case: The updated Case object with the calculated score.
    """

    query = f"{field_name}__{expression}" if expression else field_name
    return Case(
        When(**{query: value}, then=Value(score)),
        default=Value(0),
        output_field=IntegerField(),
    )
