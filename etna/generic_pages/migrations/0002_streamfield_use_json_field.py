# Generated by Django 3.2.14 on 2022-07-25 10:53

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("generic_pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "paragraph",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "link",
                                            "ol",
                                            "ul",
                                        ]
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
    ]
