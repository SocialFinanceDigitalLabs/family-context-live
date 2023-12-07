from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Person(models.Model):
    last_name = models.CharField(max_length=70, blank=True, null=True)
    first_name = models.CharField(max_length=70, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    nhs_number = models.CharField(max_length=10, blank=True, null=True)

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

    def __str__(self):
        return self.record


# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(
        User, related_name="logged_in_user", on_delete=models.CASCADE
    )
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
