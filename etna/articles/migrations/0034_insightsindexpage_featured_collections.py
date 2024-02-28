# Generated by Django 3.2.12 on 2022-03-28 14:32

from django.db import migrations
import etna.core.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0033_insightspage_insight_tag_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="insightsindexpage",
            name="featured_collections",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featuredcollection",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(max_length=100),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.TextBlock(max_length=200),
                                ),
                                (
                                    "items",
                                    etna.core.blocks.PageListBlock(
                                        "articles.InsightsPage",
                                        max_num=9,
                                        min_num=3,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
