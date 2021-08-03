# Generated by Django 3.1.8 on 2021-07-20 10:56

from django.db import migrations
import etna.media.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("insights", "0004_insightspage_hero_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="insightspage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "quote",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.core.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "quote",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=True,
                                    ),
                                ),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(
                                        max_length=100, required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "paragraph_with_heading",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.core.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("media", etna.media.blocks.EtnaMediaBlock()),
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
