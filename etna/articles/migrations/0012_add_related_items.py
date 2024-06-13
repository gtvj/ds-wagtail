# Generated by Django 3.1.8 on 2021-07-29 11:36

from django.db import migrations
import etna.articles.blocks
import etna.records.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0011_add_promoted_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="insightspage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "author",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "author",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        "authors.Author"
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "featured_record",
                        wagtail.blocks.StructBlock(
                            [("record", etna.records.blocks.RecordChooserBlock())]
                        ),
                    ),
                    (
                        "featured_records",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "introduction",
                                    wagtail.blocks.CharBlock(
                                        max_length=200, required=True
                                    ),
                                ),
                                (
                                    "records",
                                    wagtail.blocks.ListBlock(
                                        etna.records.blocks.RecordChooserBlock
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "paragraph_with_heading",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "promoted_item",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Title of the promoted page",
                                        max_length=100,
                                    ),
                                ),
                                (
                                    "category",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        "categories.Category"
                                    ),
                                ),
                                ("publication_date", wagtail.blocks.DateBlock()),
                                (
                                    "url",
                                    wagtail.blocks.URLBlock(
                                        help_text="URL for the external page",
                                        label="external URL",
                                    ),
                                ),
                                (
                                    "cta_label",
                                    wagtail.blocks.CharBlock(
                                        help_text="The button label",
                                        label="CTA label",
                                        max_length=50,
                                    ),
                                ),
                                (
                                    "teaser_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        help_text="An image used to create a teaser for the promoted page"
                                    ),
                                ),
                                (
                                    "teaser_alt_text",
                                    wagtail.blocks.CharBlock(
                                        help_text="Alt text of the teaser image",
                                        max_length=100,
                                    ),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        help_text="A description of the promoted page",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "promoted_list",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "category",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        "categories.Category"
                                    ),
                                ),
                                (
                                    "summary",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=False,
                                    ),
                                ),
                                (
                                    "promoted_items",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Title of the promoted page",
                                                        max_length=100,
                                                        required=True,
                                                    ),
                                                ),
                                                (
                                                    "description",
                                                    wagtail.blocks.RichTextBlock(
                                                        features=[
                                                            "bold",
                                                            "italic",
                                                            "link",
                                                        ],
                                                        help_text="A description of the promoted page",
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "url",
                                                    wagtail.blocks.URLBlock(
                                                        required=True
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "quote",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "quote",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        required=True,
                                    ),
                                ),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "related_items",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "related_items",
                                    wagtail.blocks.ListBlock(
                                        etna.core.blocks.RelatedItemBlock
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "section",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        help_text="Section headings must be unique within the page.",
                                        max_length=100,
                                        required=True,
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
