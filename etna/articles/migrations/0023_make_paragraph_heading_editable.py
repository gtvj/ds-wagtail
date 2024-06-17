# Generated by Django 3.1.8 on 2021-10-13 16:11
# etna:allowAlterField

from django.db import migrations
import etna.articles.blocks
import etna.media.blocks
import etna.records.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0022_make_quote_heading_optional"),
    ]

    operations = [
        migrations.AlterField(
            model_name="insightsindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "paragraph",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading_level",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("h2", "Heading level 2"),
                                            ("h3", "Heading level 3"),
                                            ("h4", "Heading level 4"),
                                        ],
                                        help_text="Use this field to select the appropriate heading tag. Check where this component will sit in the page to ensure that it follows the correct heading order and avoids skipping levels e.g. an &lt;h4&gt; should not follow an &lt;h2&gt;. For further information, see: <a href=https://www.w3.org/WAI/tutorials/page-structure/headings target=_blank>https://www.w3.org/WAI/tutorials/page-structure/headings/<a>",
                                    ),
                                ),
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link", "ul"],
                                        required=True,
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
        migrations.AlterField(
            model_name="insightspage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featured_record",
                        wagtail.blocks.StructBlock(
                            [
                                ("record", etna.records.blocks.RecordChooserBlock()),
                                (
                                    "teaser_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        help_text="Add an image to be displayed with the selected record.",
                                        required=False,
                                    ),
                                ),
                            ]
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
                        "media",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "background_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        help_text="A background image for the media block"
                                    ),
                                ),
                                ("media", etna.media.blocks.MediaChooserBlock()),
                            ]
                        ),
                    ),
                    (
                        "paragraph_with_heading",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading_level",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("h2", "Heading level 2"),
                                            ("h3", "Heading level 3"),
                                            ("h4", "Heading level 4"),
                                        ],
                                        help_text="Use this field to select the appropriate heading tag. Check where this component will sit in the page to ensure that it follows the correct heading order and avoids skipping levels e.g. an &lt;h4&gt; should not follow an &lt;h2&gt;. For further information, see: <a href=https://www.w3.org/WAI/tutorials/page-structure/headings target=_blank>https://www.w3.org/WAI/tutorials/page-structure/headings/<a>",
                                    ),
                                ),
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        max_length=100, required=True
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic", "link", "ul"],
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
                                (
                                    "publication_date",
                                    wagtail.blocks.DateBlock(required=False),
                                ),
                                (
                                    "duration",
                                    wagtail.blocks.CharBlock(
                                        help_text="Podcast or video duration. Or estimated read time of article.",
                                        label="Duration/Read time",
                                        max_length=50,
                                        required=False,
                                    ),
                                ),
                                (
                                    "url",
                                    wagtail.blocks.URLBlock(
                                        help_text="URL for the external page",
                                        label="External URL",
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
                                        max_length=100, required=False
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
                                        label="Section heading (heading level 2)",
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
