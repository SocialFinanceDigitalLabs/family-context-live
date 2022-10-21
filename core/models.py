from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceInvolvementMetadataMixin(models.Model):
    startDateOfLastInvolvement = models.DateField()
    dateOfMostRecentInteraction = models.DateField()
    DateCurrentAsOf = models.DateField()
    coverageStartDate = models.DateField()
    coverageEndDate = models.DateField()

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
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class Person(models.Model):
    cmsId = (models.CharField(max_length=50),)
    firstName = (models.CharField(max_length=70),)
    lastName = (models.CharField(max_length=70),)
    dateOfBirth = (models.DateField(),)
    gender = (
        models.CharField(
            max_length=7, choices=Gender.choices, default=Gender.NOT_SPECIFIED
        ),
    )
    address = (models.CharField(max_length=256),)
    otherFields = (models.JSONField(encoder=DjangoJSONEncoder, default=dict),)
    relation = models.ManyToManyField(
        "self", through="PersonRelationship", through_fields=("person", "relation")
    )


class PersonRelationship(models.Model):
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="relationships"
    )
    relation = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="reverse_relationships"
    )
    relationType = models.CharField(
        max_length=15,
        choices=RelationshipType.choices,
        default=RelationshipType.NOT_SPECIFIED,
    )


class ServiceSummary(models.Model):
    person = (models.ForeignKey("Person", on_delete=models.CASCADE),)
    title = models.CharField(max_length=50)
    lastSynchronised = models.DateTimeField()
    coverageStartDate = models.DateField()
    coverageEndDate = models.DateField()
    dataSource = models.CharField(max_length=70)
    recordsAvailable = models.BooleanField()
    coverageExplanation = models.CharField(max_length=70)
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class Police(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    policeArea = models.CharField(max_length=50)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class OffenceSummary(models.Model):
    police = models.ForeignKey(
        "Police", related_name="safeguardingOffences", on_delete=models.CASCADE
    )
    dateOfOffence = models.DateField()
    typeOfOffence = models.CharField(max_length=70)
    natureOfInvolvement = models.CharField(max_length=70)
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class OffenceRecords(models.Model):
    police = models.ForeignKey(
        Police, related_name="nonSafeGuardingOffences", on_delete=models.CASCADE
    )
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class AdultSocialCare(ServiceInvolvementMetadataMixin, models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    serviceInvolvement = models.CharField(
        choices=ServiceInvolvement.choices,
        max_length=15,
        default=ServiceInvolvement.NOT_SPECIFIED,
    )
    localAuthorityOrganisation = models.CharField(max_length=50)
    contact = models.ForeignKey(
        "Contact", related_name="contactFor", on_delete=models.CASCADE
    )
    coverageGeographicArea = models.CharField(max_length=70)
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class School(ServiceInvolvementMetadataMixin, models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    serviceInvolvement = models.CharField(
        choices=ServiceInvolvement.choices,
        max_length=15,
        default=ServiceInvolvement.NOT_SPECIFIED,
    )
    schoolName = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=20)
    admissionType = models.CharField(max_length=50)
    coverageGeographicArea = models.DateField()
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)


class Housing(ServiceInvolvementMetadataMixin, models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    serviceInvolvement = models.CharField(
        choices=ServiceInvolvement.choices,
        max_length=15,
        default=ServiceInvolvement.NOT_SPECIFIED,
    )
    housingAssociation = models.CharField(max_length=100)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    tenancyStart = models.DateField()
    antiSocialBehaviour = models.BooleanField(default=False)
    rentArrears = models.BooleanField(default=False)
    noticeSeekingPossession = models.BooleanField(default=False)
    eviction = models.BooleanField(default=False)
    coverageGeographicArea = models.CharField(max_length=100)
    otherFields = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
