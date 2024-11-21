# Generated by Django 5.1.2 on 2024-11-21 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_openingtimes"),
        ("whatson", "0015_exhibitionpage_related_pages_exhibitionpage_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="exhibitionpage",
            name="opening_times",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="core.openingtimes",
            ),
        ),
    ]
