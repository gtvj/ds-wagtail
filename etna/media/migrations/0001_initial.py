# Generated by Django 3.1.8 on 2021-08-03 11:11

import django.core.validators
import django.db.models.deletion
import taggit.managers
import wagtail.fields
import wagtail.models
import wagtail.search.index
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
    ]

    operations = [
        migrations.CreateModel(
            name="EtnaMedia",
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
                    "title",
                    models.CharField(max_length=255, verbose_name="title"),
                ),
                (
                    "file",
                    models.FileField(upload_to="media", verbose_name="file"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("audio", "Audio file"),
                            ("video", "Video file"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "duration",
                    models.FloatField(
                        blank=True,
                        default=0,
                        help_text="Duration in seconds",
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="duration",
                    ),
                ),
                (
                    "width",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="width"
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="height"
                    ),
                ),
                (
                    "thumbnail",
                    models.FileField(
                        blank=True,
                        upload_to="media_thumbnails",
                        verbose_name="thumbnail",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created at"
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "description",
                    wagtail.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "transcript",
                    wagtail.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        default=wagtail.models.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "verbose_name": "media",
                "abstract": False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
