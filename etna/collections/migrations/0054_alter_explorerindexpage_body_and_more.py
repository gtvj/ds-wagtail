# Generated by Django 5.0.3 on 2024-04-03 10:30
# etna:allowAlterField

import etna.core.blocks.page_chooser
import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0053_alter_explorerindexpage_featured_article_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="explorerindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "large_card_links",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=False
                                    ),
                                ),
                                (
                                    "page_1",
                                    etna.core.blocks.page_chooser.APIPageChooserBlock(
                                        label="Link one target"
                                    ),
                                ),
                                (
                                    "page_2",
                                    etna.core.blocks.page_chooser.APIPageChooserBlock(
                                        label="Link two target"
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "large_card_links",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=False
                                    ),
                                ),
                                (
                                    "page_1",
                                    etna.core.blocks.page_chooser.APIPageChooserBlock(
                                        label="Link one target"
                                    ),
                                ),
                                (
                                    "page_2",
                                    etna.core.blocks.page_chooser.APIPageChooserBlock(
                                        label="Link two target"
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "large_card_links",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=False
                                    ),
                                ),
                                (
                                    "page_1",
                                    etna.core.blocks.page_chooser.APIPageChooserBlock(
                                        label="Link one target"
                                    ),
                                ),
                                (
                                    "page_2",
                                    etna.core.blocks.page_chooser.APIPageChooserBlock(
                                        label="Link two target"
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
    ]
