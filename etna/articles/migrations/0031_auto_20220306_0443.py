# Generated by Django 3.2.12 on 2022-03-06 04:43

import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0020_rename_result_page_record_relationship"),
        ("articles", "0030_insightsindexpage_featured_insight"),
    ]

    operations = [
        migrations.CreateModel(
            name="InsightsTag",
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
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="name"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=100, unique=True, verbose_name="slug"
                    ),
                ),
            ],
            options={
                "verbose_name": "insights tag",
                "verbose_name_plural": "insights tags",
            },
        ),
        migrations.AddField(
            model_name="insightspage",
            name="time_period",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="collections.timeperiodexplorerpage",
            ),
        ),
        migrations.AddField(
            model_name="insightspage",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="collections.topicexplorerpage",
            ),
        ),
        migrations.CreateModel(
            name="TaggedInsights",
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
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged_items",
                        to="articles.insightspage",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged_insights",
                        to="articles.insightstag",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="insightspage",
            name="tags",
            field=modelcluster.contrib.taggit.ClusterTaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="articles.TaggedInsights",
                to="articles.InsightsTag",
                verbose_name="Tags",
            ),
        ),
    ]
