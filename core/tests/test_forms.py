from django.test import TestCase
from core.forms import NameSearchForm, NHSIdForm


class NameSearchFormTest(TestCase):
    def test_last_name_field_label(self):
        form = NameSearchForm()
        self.assertTrue(
            form.fields["last_name"].label is None
            or form.fields["last_name"].label == "Family Name"
        )

    def test_first_name_field_label(self):
        form = NameSearchForm()
        self.assertTrue(
            form.fields["first_name"].label is None
            or form.fields["first_name"].label == "First Name"
        )

    def test_date_of_birth_field_label(self):
        form = NameSearchForm()
        self.assertTrue(
            form.fields["date_of_birth"].label is None
            or form.fields["date_of_birth"].label == "Date of Birth (optional)"
        )


class NHSIdFormTest(TestCase):
    def test_nhs_number_field_label(self):
        form = NHSIdForm()
        self.assertTrue(
            form.fields["nhs_number"].label is None
            or form.fields["nhs_number"].label == "NHS number"
        )
