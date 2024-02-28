# Generated by Django 3.1.8 on 2021-07-12 13:38

import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0011_explorerindexpage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="resultspagerecordpage",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Optional field to override the description for this record in the teaser.",
            ),
        ),
        migrations.AlterField(
            model_name="explorerindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "time_period_explorer",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        default="Explore by time period",
                                        max_length=100,
                                    ),
                                ),
                                (
                                    "sub_heading",
                                    wagtail.blocks.CharBlock(
                                        default="The National Archives contains over 1,000 years of British historical records. Select a time period to start exploring.",
                                        max_length=200,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "topic_explorer_explorer",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        default="Explore by topic",
                                        max_length=100,
                                    ),
                                ),
                                (
                                    "sub_heading",
                                    wagtail.blocks.CharBlock(
                                        default="Discover highlights of The National Archives’ collections.",
                                        max_length=200,
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
    ]
