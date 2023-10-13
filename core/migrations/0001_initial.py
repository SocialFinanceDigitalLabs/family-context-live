# Generated by Django 4.2.5 on 2023-10-13 10:08

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=20)),
                ("role", models.CharField(max_length=20)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DataSource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=70, null=True)),
                ("last_update", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_name", models.CharField(blank=True, max_length=70, null=True)),
                ("first_name", models.CharField(blank=True, max_length=70, null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("address", models.CharField(blank=True, max_length=256, null=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                ("nhs_number", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ServiceSummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("last_synchronised", models.DateTimeField()),
                ("coverage_start_date", models.DateField()),
                ("coverage_end_date", models.DateField()),
                ("data_source", models.CharField(max_length=70)),
                ("records_available", models.BooleanField()),
                ("coverage_explanation", models.CharField(max_length=70)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date_of_last_involvement", models.DateField()),
                ("date_of_most_recent_interaction", models.DateField()),
                ("date_current_as_of", models.DateField()),
                ("coverage_start_date", models.DateField()),
                ("coverage_end_date", models.DateField()),
                (
                    "service_involvement",
                    models.CharField(
                        choices=[
                            ("Current", "Current"),
                            ("Historic", "Historic"),
                            ("Not Specified", "Not Specified"),
                        ],
                        default="Not Specified",
                        max_length=15,
                    ),
                ),
                ("school_name", models.CharField(max_length=100)),
                ("contact_number", models.CharField(max_length=20)),
                ("admission_type", models.CharField(max_length=50)),
                ("coverage_geographic_area", models.CharField(max_length=100)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="school",
                        to="core.person",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_school_records",
                        to="core.servicesummary",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("record", models.JSONField()),
                (
                    "datasource_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.datasource",
                    ),
                ),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.person"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Police",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("police_area", models.CharField(max_length=50)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.contact"
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="police",
                        to="core.person",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_police_records",
                        to="core.servicesummary",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OffenceSummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_offence", models.DateField()),
                ("type_of_offence", models.CharField(max_length=70)),
                ("nature_of_involvement", models.CharField(max_length=70)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "police",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="safeguarding_offences",
                        to="core.police",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OffenceRecords",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "police",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="non_safeguarding_offences",
                        to="core.police",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Housing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date_of_last_involvement", models.DateField()),
                ("date_of_most_recent_interaction", models.DateField()),
                ("date_current_as_of", models.DateField()),
                ("coverage_start_date", models.DateField()),
                ("coverage_end_date", models.DateField()),
                (
                    "service_involvement",
                    models.CharField(
                        choices=[
                            ("Current", "Current"),
                            ("Historic", "Historic"),
                            ("Not Specified", "Not Specified"),
                        ],
                        default="Not Specified",
                        max_length=15,
                    ),
                ),
                ("housing_association", models.CharField(max_length=100)),
                ("tenancy_start", models.DateField()),
                ("antisocial_behaviour", models.BooleanField(default=False)),
                ("rent_arrears", models.BooleanField(default=False)),
                ("notice_seeking_possession", models.BooleanField(default=False)),
                ("eviction", models.BooleanField(default=False)),
                ("coverage_geographic_area", models.CharField(max_length=100)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.contact"
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="housing",
                        to="core.person",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_housing_records",
                        to="core.servicesummary",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AdultSocialCare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date_of_last_involvement", models.DateField()),
                ("date_of_most_recent_interaction", models.DateField()),
                ("date_current_as_of", models.DateField()),
                ("coverage_start_date", models.DateField()),
                ("coverage_end_date", models.DateField()),
                (
                    "service_involvement",
                    models.CharField(
                        choices=[
                            ("Current", "Current"),
                            ("Historic", "Historic"),
                            ("Not Specified", "Not Specified"),
                        ],
                        default="Not Specified",
                        max_length=15,
                    ),
                ),
                ("local_authority_organisation", models.CharField(max_length=50)),
                ("coverage_geographic_area", models.CharField(max_length=70)),
                (
                    "other",
                    models.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contact_for",
                        to="core.contact",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="adult_social_care",
                        to="core.person",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_adult_social_care_records",
                        to="core.servicesummary",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]