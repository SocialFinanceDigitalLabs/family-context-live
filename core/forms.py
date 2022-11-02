import datetime

from django import forms

years = range(datetime.date.today().year - 120, datetime.date.today().year)


class NameSearchForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=70)
    last_name = forms.CharField(label="Family Name", max_length=70)
    date_of_birth = forms.DateField(
        label="Date of Birth (optional)",
        widget=forms.SelectDateWidget(years=years),
        required=False,
    )


class CmsIdForm(forms.Form):
    cms_id = forms.CharField(label="CMS ID", max_length=50)
