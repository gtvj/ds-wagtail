# Generated by Django 3.1.8 on 2021-08-11 10:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("records", "0011_remove_date_start_and_end_rename_date_range"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordpage",
            name="topics",
            field=models.JSONField(null=True),
        ),
    ]
