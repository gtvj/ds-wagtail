# Generated by Django 3.1.8 on 2021-07-23 13:04

from django.db import migrations
import etna.home.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_add_alerts"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featured_items",
                        wagtail.blocks.ListBlock(
                            etna.home.blocks.FeaturedItemBlock
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
