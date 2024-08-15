# Generated by Django 5.0.8 on 2024-08-15 09:20

import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0008_personpage_first_name_personpage_last_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoleChoices",
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
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Role choice",
                "verbose_name_plural": "Role choices",
            },
        ),
        migrations.AddField(
            model_name="personpage",
            name="research_specialism",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="personpage",
            name="research_summary",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="personpage",
            name="role_overrides",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="people.rolechoices"
            ),
        ),
    ]
