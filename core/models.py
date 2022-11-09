from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceInvolvementMetadataMixin(models.Model):
    start_date_of_last_involvement = models.DateField()
    date_of_most_recent_interaction = models.DateField()
    date_current_as_of = models.DateField()
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()

    class Meta:
        abstract = True


class Gender(models.TextChoices):
    MALE = (
        "M",
        _("Male"),
    )
    FEMALE = (
        "F",
        _("Female"),
    )
    OTHER = (
        "O",
        _("Other"),
    )
    NOT_SPECIFIED = "U", _("Not Specified")


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


class Person(models.Model):
    cms_id = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=70, blank=True, null=True)
    last_name = models.CharField(max_length=70, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=7, choices=Gender.choices, default=Gender.NOT_SPECIFIED
    )
    address = models.CharField(max_length=256, blank=True, null=True)
    other_fields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
    relation = models.ManyToManyField(
        "self", through="PersonRelationship", through_fields=("person", "relation")
    )

    @property
    def age(self):
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)


class PersonRelationship(models.Model):
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="relationships"
    )
    relation = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="reverse_relationships"
    )
    relation_type = models.CharField(
        max_length=15,
        choices=RelationshipType.choices,
        default=RelationshipType.NOT_SPECIFIED,
    )


class ServiceSummary(models.Model):
    person = (models.ForeignKey("Person", on_delete=models.CASCADE),)
    title = models.CharField(max_length=50)
    last_synchronised = models.DateTimeField()
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()
    data_source = models.CharField(max_length=70)
    records_available = models.BooleanField()
    coverage_explanation = models.CharField(max_length=70)
    other = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class Police(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
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
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
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
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
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
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
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
