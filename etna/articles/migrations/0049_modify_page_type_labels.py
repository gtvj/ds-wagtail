# Generated by Django 4.0.8 on 2023-02-02 16:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0048_add_recordarticlepage_and_pagegalleryimage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="articlepage",
            options={"verbose_name": "article", "verbose_name_plural": "articles"},
        ),
        migrations.AlterModelOptions(
            name="recordarticlepage",
            options={
                "verbose_name": "record article",
                "verbose_name_plural": "record articles",
            },
        ),
    ]
