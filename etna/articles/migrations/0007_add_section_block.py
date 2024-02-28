# Generated by Django 3.1.8 on 2021-07-23 10:52

import etna.records.blocks
import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0006_record_embed_blocks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="insightspage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "quote",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "quote",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=True,
                                    ),
                                ),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "paragraph_with_heading",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "section",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        help_text="Section headings must be unique within the page.",
                                        max_length=100,
                                        required=True,
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "featured_record",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "record",
                                    etna.records.blocks.RecordChooserBlock(),
                                )
                            ]
                        ),
                    ),
                    (
                        "featured_records",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "introduction",
                                    wagtail.blocks.CharBlock(
                                        max_length=200, required=True
                                    ),
                                ),
                                (
                                    "records",
                                    wagtail.blocks.ListBlock(
                                        etna.records.blocks.RecordChooserBlock
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
