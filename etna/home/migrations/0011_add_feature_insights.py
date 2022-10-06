# Generated by Django 3.2.14 on 2022-08-02 21:07

from django.db import migrations, models
import django.db.models.deletion
import etna.core.blocks.page_list
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("insights", "0043_streamfield_use_json_field"),
        ("home", "0010_streamfield_use_json_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="featured_collections",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featuredcollection",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "items",
                                    etna.core.blocks.page_list.PageListBlock(
                                        "insights.InsightsPage", max_num=9, min_num=3
                                    ),
                                )
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="featured_insight",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="insights.insightspage",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="sub_heading",
            field=models.CharField(
                default="Discover some of the most important and unusual records from over 1000 years of history.",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "time_period",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        default="Explore by time period", max_length=100
                                    ),
                                ),
                                (
                                    "sub_heading",
                                    wagtail.blocks.CharBlock(
                                        default="Discover 1,000 years of British history through time periods including:",
                                        max_length=200,
                                    ),
                                ),
                                (
                                    "page",
                                    wagtail.blocks.PageChooserBlock(
                                        page_type=[
                                            "collections.TimePeriodExplorerIndexPage"
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "topic_explorer",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        default="Explore by topic", max_length=100
                                    ),
                                ),
                                (
                                    "sub_heading",
                                    wagtail.blocks.CharBlock(
                                        default="Browse highlights of the collection through topics including:",
                                        max_length=200,
                                    ),
                                ),
                                (
                                    "page",
                                    wagtail.blocks.PageChooserBlock(
                                        page_type=["collections.TopicExplorerIndexPage"]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "paragraph",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link", "ul"]
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
