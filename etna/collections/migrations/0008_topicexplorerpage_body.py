# Generated by Django 3.1.8 on 2021-07-09 14:22

from django.db import migrations
import etna.collections.blocks
import etna.core.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0007_add_alerts"),
    ]

    operations = [
        migrations.AddField(
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
                                        default="Collection Highlights", max_length=100
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
