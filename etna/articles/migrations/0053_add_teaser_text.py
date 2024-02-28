# Generated by Django 4.0.8 on 2023-02-16 15:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "articles",
            "0052_remove_pagegalleryimage_transcription_header_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="articleindexpage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="articlepage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recordarticlepage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
    ]
