# Generated by Django 3.2.12 on 2022-03-04 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0029_migrate_hero_image_alt_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="insightsindexpage",
            name="featured_insight",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="articles.insightspage",
            ),
        ),
    ]
