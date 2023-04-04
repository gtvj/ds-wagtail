# Generated by Django 4.0.8 on 2022-11-03 17:44

from django.db import migrations
import etna.core.blocks.page_list
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0045_add_search_image_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="insightsindexpage",
            name="featured_collections",
        ),
        migrations.AddField(
            model_name="insightsindexpage",
            name="featured_pages",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featuredpages",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(max_length=100)),
                                (
                                    "description",
                                    wagtail.blocks.TextBlock(max_length=200),
                                ),
                                (
                                    "items",
                                    etna.core.blocks.page_list.PageListBlock(
                                        "articles.InsightsPage", max_num=9, min_num=3
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
