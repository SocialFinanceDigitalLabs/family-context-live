from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    last_name = models.CharField(max_length=70, blank=True, null=True)
    first_name = models.CharField(max_length=70, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    nhs_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.last_name


class DataSource(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    last_update = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Record(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    datasource_id = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    record = models.JSONField()


class ServiceInvolvementMetadataMixin(models.Model):
    start_date_of_last_involvement = models.DateField()
    date_of_most_recent_interaction = models.DateField()
    date_current_as_of = models.DateField()
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()

    class Meta:
        abstract = True


class RelationshipType(models.TextChoices):
    SIBLING = "Sibling", _("Sibling")
    PARENT = "Parent", _("Parent")
    CHILD = "Child", _("Child")
    GRANDPARENT = "Grandparent", _("Grandparent")
    OTHER = "Other", _("Other")
    NOT_SPECIFIED = "Not Specified", _("Not Specified")


class ServiceInvolvement(models.TextChoices):
    CURRENT = (
        "Current",
        _("Current"),
    )
    HISTORIC = "Historic", _("Historic")
    NOT_SPECIFIED = "Not Specified", _("Not Specified")


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


# class PersonRelationship(models.Model):
#     person = models.ForeignKey(
#         "Person", on_delete=models.CASCADE, related_name="relationships"
#     )
#     relation = models.ForeignKey(
#         "Person", on_delete=models.CASCADE, related_name="reverse_relationships"
#     )
#     relation_type = models.CharField(
#         max_length=15,
#         choices=RelationshipType.choices,
#         default=RelationshipType.NOT_SPECIFIED,
#     )


class ServiceSummary(models.Model):
    title = models.CharField(max_length=50)
    last_synchronised = models.DateTimeField()
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()
    data_source = models.CharField(max_length=70)
    records_available = models.BooleanField()
    coverage_explanation = models.CharField(max_length=70)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class Police(models.Model):
    service = models.ForeignKey(
        "ServiceSummary",
        on_delete=models.CASCADE,
        related_name="service_police_records",
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="police"
    )
    police_area = models.CharField(max_length=50)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class OffenceSummary(models.Model):
    police = models.ForeignKey(
        "Police", related_name="safeguarding_offences", on_delete=models.CASCADE
    )
    date_of_offence = models.DateField()
    type_of_offence = models.CharField(max_length=70)
    nature_of_involvement = models.CharField(max_length=70)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class OffenceRecords(models.Model):
    police = models.ForeignKey(
        Police, related_name="non_safeguarding_offences", on_delete=models.CASCADE
    )
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class AdultSocialCare(ServiceInvolvementMetadataMixin, models.Model):
    service = models.ForeignKey(
        "ServiceSummary",
        on_delete=models.CASCADE,
        related_name="service_adult_social_care_records",
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="adult_social_care"
    )
    service_involvement = models.CharField(
        choices=ServiceInvolvement.choices,
        max_length=15,
        default=ServiceInvolvement.NOT_SPECIFIED,
    )
    local_authority_organisation = models.CharField(max_length=50)
    contact = models.ForeignKey(
        "Contact", related_name="contact_for", on_delete=models.CASCADE
    )
    coverage_geographic_area = models.CharField(max_length=70)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class School(ServiceInvolvementMetadataMixin, models.Model):
    service = models.ForeignKey(
        "ServiceSummary",
        on_delete=models.CASCADE,
        related_name="service_school_records",
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="school")
    service_involvement = models.CharField(
        choices=ServiceInvolvement.choices,
        max_length=15,
        default=ServiceInvolvement.NOT_SPECIFIED,
    )
    school_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    admission_type = models.CharField(max_length=50)
    coverage_geographic_area = models.CharField(max_length=100)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class Housing(ServiceInvolvementMetadataMixin, models.Model):
    service = models.ForeignKey(
        "ServiceSummary",
        on_delete=models.CASCADE,
        related_name="service_housing_records",
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="housing"
    )
    service_involvement = models.CharField(
        choices=ServiceInvolvement.choices,
        max_length=15,
        default=ServiceInvolvement.NOT_SPECIFIED,
    )
    housing_association = models.CharField(max_length=100)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    tenancy_start = models.DateField()
    antisocial_behaviour = models.BooleanField(default=False)
    rent_arrears = models.BooleanField(default=False)
    notice_seeking_possession = models.BooleanField(default=False)
    eviction = models.BooleanField(default=False)
    coverage_geographic_area = models.CharField(max_length=100)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
