# Generated by Django 5.0.4 on 2024-05-07 08:40
# etna:allowAlterField

import etna.core.blocks.page_chooser
import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0056_alter_highlightgallerypage_featured_article"),
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
                                        label="Link one target",
                                        required_api_fields=["teaser_image"],
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
                                        label="Link one target",
                                        required_api_fields=["teaser_image"],
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
                                        label="Link one target",
                                        required_api_fields=["teaser_image"],
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
