import datetime

from django import forms

years = range(datetime.date.today().year - 120, datetime.date.today().year)


class NameSearchForm(forms.Form):
    last_name = forms.CharField(label="Family Name", max_length=70)
    first_name = forms.CharField(label="First Name", max_length=70)
    date_of_birth = forms.DateField(
        label="Date of Birth (optional)",
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False,
    )


class NHSIdForm(forms.Form):
    nhs_number = forms.CharField(label="NHS number", max_length=50)
