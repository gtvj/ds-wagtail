# Generated by Django 5.0.7 on 2024-07-22 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0001_initial"),
        ("generic_pages", "0025_hubpage_body_hubpage_hero_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="generalpage",
            name="alert",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="alerts.alert",
            ),
        ),
        migrations.AddField(
            model_name="hubpage",
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
