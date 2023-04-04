# Generated by Django 4.0.8 on 2023-02-15 13:58

from django.db import migrations, models
import django.db.models.deletion
import etna.analytics.mixins
import etna.collections.models
import modelcluster.fields
import wagtail.fields
import wagtailmetadata.models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("images", "0004_remove_customimage_translation_language_and_more"),
        ("articles", "0052_remove_pagegalleryimage_transcription_header_and_more"),
        ("collections", "0028_swap_image_reference_fields_to_new_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="HighlightGalleryPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "intro",
                    wagtail.fields.RichTextField(
                        help_text="1-2 sentences introducing the subject of the article and explaining why a user should read on.",
                        max_length=300,
                        verbose_name="introductory text",
                    ),
                ),
                (
                    "teaser_text",
                    models.TextField(
                        help_text="A short, enticing description of the article. This will appear in promos and under thumbnails around the site.",
                        max_length=160,
                        verbose_name="teaser text",
                    ),
                ),
                (
                    "featured_article",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="articles.articlepage",
                        verbose_name="featured article",
                    ),
                ),
                (
                    "featured_record_article",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="articles.recordarticlepage",
                        verbose_name="featured record article",
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.customimage",
                        verbose_name="Search image",
                    ),
                ),
                (
                    "teaser_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.customimage",
                    ),
                ),
            ],
            options={
                "verbose_name": "highlight gallery page",
                "verbose_name_plural": "highlight gallery pages",
            },
            bases=(
                etna.collections.models.TopicalPageMixin,
                wagtailmetadata.models.WagtailImageMetadataMixin,
                etna.analytics.mixins.DataLayerMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Highlight",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "long_description",
                    wagtail.fields.RichTextField(
                        max_length=400, verbose_name="long description"
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="images.customimage",
                        verbose_name="image",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page_highlights",
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]
