# Generated by Django 3.1.8 on 2021-07-22 09:39

from django.db import migrations
import etna.records.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("insights", "0005_rename_title_to_heading"),
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
                    (
                        "featured_record",
                        wagtail.core.blocks.StructBlock(
                            [("record", etna.records.blocks.RecordChooserBlock())]
                        ),
                    ),
                    (
                        "featured_records",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.core.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "introduction",
                                    wagtail.core.blocks.CharBlock(
                                        max_length=200, required=True
                                    ),
                                ),
                                (
                                    "records",
                                    wagtail.core.blocks.ListBlock(
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
