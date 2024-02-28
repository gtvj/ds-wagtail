# Generated by Django 3.1.8 on 2021-08-13 09:47

import etna.collections.blocks
import etna.core.blocks
import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0017_add_time_period_topic_index_page_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timeperiodexplorerpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "collection_highlights",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        default="Collection Highlights",
                                        max_length=100,
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "featured_page",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(max_length=100),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.CharBlock(
                                        help_text="A description of the featured page",
                                        max_length=200,
                                        required=False,
                                    ),
                                ),
                                ("page", wagtail.blocks.PageChooserBlock()),
                            ]
                        ),
                    ),
                    (
                        "promoted_pages",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(max_length=100),
                                ),
                                (
                                    "sub_heading",
                                    wagtail.blocks.CharBlock(max_length=200),
                                ),
                                (
                                    "promoted_items",
                                    wagtail.blocks.ListBlock(
                                        etna.core.blocks.PromotedLinkBlock,
                                        max=3,
                                        min=3,
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "collection_highlights",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        default="Collection Highlights",
                                        max_length=100,
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "featured_page",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(max_length=100),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.CharBlock(
                                        help_text="A description of the featured page",
                                        max_length=200,
                                        required=False,
                                    ),
                                ),
                                ("page", wagtail.blocks.PageChooserBlock()),
                            ]
                        ),
                    ),
                    (
                        "promoted_pages",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(max_length=100),
                                ),
                                (
                                    "sub_heading",
                                    wagtail.blocks.CharBlock(max_length=200),
                                ),
                                (
                                    "promoted_items",
                                    wagtail.blocks.ListBlock(
                                        etna.core.blocks.PromotedLinkBlock,
                                        max=3,
                                        min=3,
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
