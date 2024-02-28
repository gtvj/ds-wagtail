# Generated by Django 3.1.8 on 2021-07-09 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alerts", "0001_initial"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="alert",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="alerts.alert",
            ),
        ),
    ]
