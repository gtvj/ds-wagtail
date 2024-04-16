# Generated by Django 5.0.3 on 2024-04-11 10:02
# etna:allowAlterField

import etna.core.blocks.page_chooser
import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("whatson", "0009_alter_eventpage_venue_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="whatsonpage",
            name="large_card_links",
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
