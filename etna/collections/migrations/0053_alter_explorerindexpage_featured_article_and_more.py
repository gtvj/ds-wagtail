# Generated by Django 4.2.5 on 2023-10-17 13:45

import django.db.models.deletion
import etna.core.blocks.page_list
import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("collections", "0052_add_model_verbose_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="explorerindexpage",
            name="featured_article",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a page to display in the featured area. This can be an Article, Focused Article or Record Article.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
                verbose_name="featured article",
            ),
        ),
        migrations.AlterField(
            model_name="explorerindexpage",
            name="featured_articles",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featuredarticles",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "items",
                                    etna.core.blocks.page_list.PageListBlock(
                                        "articles.ArticlePage",
                                        "articles.RecordArticlePage",
                                        "articles.FocusedArticlePage",
                                        max_num=6,
                                        min_num=3,
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
        migrations.AlterField(
            model_name="highlightgallerypage",
            name="featured_article",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a page to display in the featured area. This can be an Article or Focused Article.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
                verbose_name="featured article",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerpage",
            name="featured_article",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a page to display in the featured area. This can be an Article or Focused Article.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
                verbose_name="featured article",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerpage",
            name="featured_article",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a page to display in the featured area. This can be an Article or Focused Article.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
                verbose_name="featured article",
            ),
        ),
    ]
