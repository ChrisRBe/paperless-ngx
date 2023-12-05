# Generated by Django 4.2.6 on 2023-11-02 17:38

import django.db.models.deletion
import django.utils.timezone
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.db import migrations
from django.db import models
from django.db.models import Q


def add_customfield_permissions(apps, schema_editor):
    # create permissions without waiting for post_migrate signal
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    add_permission = Permission.objects.get(codename="add_document")
    customfield_permissions = Permission.objects.filter(
        codename__contains="customfield",
    )

    for user in User.objects.filter(Q(user_permissions=add_permission)).distinct():
        user.user_permissions.add(*customfield_permissions)

    for group in Group.objects.filter(Q(permissions=add_permission)).distinct():
        group.permissions.add(*customfield_permissions)


def remove_customfield_permissions(apps, schema_editor):
    customfield_permissions = Permission.objects.filter(
        codename__contains="customfield",
    )

    for user in User.objects.all():
        user.user_permissions.remove(*customfield_permissions)

    for group in Group.objects.all():
        group.permissions.remove(*customfield_permissions)


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "1039_consumptiontemplate"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                (
                    "data_type",
                    models.CharField(
                        choices=[
                            ("string", "String"),
                            ("url", "URL"),
                            ("date", "Date"),
                            ("boolean", "Boolean"),
                            ("integer", "Integer"),
                            ("float", "Float"),
                            ("monetary", "Monetary"),
                        ],
                        editable=False,
                        max_length=50,
                        verbose_name="data type",
                    ),
                ),
            ],
            options={
                "verbose_name": "custom field",
                "verbose_name_plural": "custom fields",
                "ordering": ("created",),
            },
        ),
        migrations.CreateModel(
            name="CustomFieldInstance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                ("value_text", models.CharField(max_length=128, null=True)),
                ("value_bool", models.BooleanField(null=True)),
                ("value_url", models.URLField(null=True)),
                ("value_date", models.DateField(null=True)),
                ("value_int", models.IntegerField(null=True)),
                ("value_float", models.FloatField(null=True)),
                (
                    "value_monetary",
                    models.DecimalField(decimal_places=2, max_digits=12, null=True),
                ),
                (
                    "document",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="custom_fields",
                        to="documents.document",
                    ),
                ),
                (
                    "field",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="documents.customfield",
                    ),
                ),
            ],
            options={
                "verbose_name": "custom field instance",
                "verbose_name_plural": "custom field instances",
                "ordering": ("created",),
            },
        ),
        migrations.AddConstraint(
            model_name="customfield",
            constraint=models.UniqueConstraint(
                fields=("name",),
                name="documents_customfield_unique_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="customfieldinstance",
            constraint=models.UniqueConstraint(
                fields=("document", "field"),
                name="documents_customfieldinstance_unique_document_field",
            ),
        ),
        migrations.RunPython(
            add_customfield_permissions,
            remove_customfield_permissions,
        ),
    ]