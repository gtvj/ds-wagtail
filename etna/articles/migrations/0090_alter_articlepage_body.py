# Generated by Django 4.2.1 on 2023-06-07 10:58

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
        ("articles", "0089_alter_articleindexpage_featured_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "content_section",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        label="Heading", max_length=100
                                    ),
                                ),
                                (
                                    "content",
                                    wagtail.blocks.StreamBlock(
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
                                            ),
                                            (
                                                "quote",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "quote",
                                                            wagtail.blocks.RichTextBlock(
                                                                features=[
                                                                    "bold",
                                                                    "italic",
                                                                    "link",
                                                                ],
                                                                required=True,
                                                            ),
                                                        ),
                                                        (
                                                            "attribution",
                                                            wagtail.blocks.CharBlock(
                                                                max_length=100,
                                                                required=False,
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "sub_heading",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "heading",
                                                            wagtail.blocks.CharBlock(
                                                                label="Sub-heading",
                                                                max_length=100,
                                                            ),
                                                        )
                                                    ]
                                                ),
                                            ),
                                            (
                                                "image",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "alt_text",
                                                            wagtail.blocks.CharBlock(
                                                                help_text='Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                                                                label="Alternative text",
                                                                max_length=100,
                                                            ),
                                                        ),
                                                        (
                                                            "caption",
                                                            wagtail.blocks.RichTextBlock(
                                                                features=[
                                                                    "bold",
                                                                    "italic",
                                                                    "link",
                                                                ],
                                                                help_text="If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.",
                                                                label="Caption (optional)",
                                                                required=False,
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
                                                            "title",
                                                            wagtail.blocks.CharBlock(
                                                                help_text="A descriptive title for the media block",
                                                                required=True,
                                                            ),
                                                        ),
                                                        (
                                                            "background_image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                help_text="A background image for the media block"
                                                            ),
                                                        ),
                                                        (
                                                            "media",
                                                            etna.media.blocks.MediaChooserBlock(),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "featured_record_article",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "page",
                                                            wagtail.blocks.PageChooserBlock(
                                                                label="Page",
                                                                page_type=[
                                                                    "articles.RecordArticlePage"
                                                                ],
                                                            ),
                                                        )
                                                    ]
                                                ),
                                            ),
                                            (
                                                "featured_record",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(
                                                                help_text="A short description (max 200 characters) to add 'relevancy' to the record details. For example: 'Entry for Alice Hawkins in the index to suffragettes arrested'.",
                                                                label="Descriptive title",
                                                                max_length=200,
                                                            ),
                                                        ),
                                                        (
                                                            "record",
                                                            etna.records.blocks.RecordChooserBlock(),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.blocks.StructBlock(
                                                                [
                                                                    (
                                                                        "image",
                                                                        wagtail.images.blocks.ImageChooserBlock(
                                                                            required=False
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "decorative",
                                                                        wagtail.blocks.BooleanBlock(
                                                                            default=False,
                                                                            help_text='Decorative images are used for visual effect and do not add information to the content of a page. <a href="https://www.w3.org/WAI/tutorials/images/decorative/" target="_blank">"Check the guidance to see if your image is decorative</a>.',
                                                                            label="Is this image decorative? <p class='field-title__subheading'>Tick the box if 'yes'</p>",
                                                                            required=False,
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "alt_text",
                                                                        wagtail.blocks.CharBlock(
                                                                            help_text='Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. Decorative images do not require alt text. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                                                                            label="Image alternative text",
                                                                            max_length=100,
                                                                            required=False,
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "caption",
                                                                        wagtail.blocks.RichTextBlock(
                                                                            features=[
                                                                                "bold",
                                                                                "italic",
                                                                                "link",
                                                                            ],
                                                                            help_text="An optional caption for non-decorative images, which will be displayed directly below the image. This could be used for image sources or for other useful metadata.",
                                                                            label="Caption (optional)",
                                                                            required=False,
                                                                        ),
                                                                    ),
                                                                ],
                                                                help_text="Add an image to be displayed with the selected record.",
                                                                label="Teaser image",
                                                                required=False,
                                                                template="articles/blocks/images/blog-embed__image-container.html",
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
                                                            "introduction",
                                                            wagtail.blocks.CharBlock(
                                                                max_length=200,
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "items",
                                                            wagtail.blocks.ListBlock(
                                                                etna.articles.blocks.FeaturedRecordsItemBlock
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
                                                                label="Title",
                                                                max_length=100,
                                                            ),
                                                        ),
                                                        (
                                                            "category",
                                                            wagtail.blocks.ChoiceBlock(
                                                                choices=[
                                                                    (
                                                                        "blog",
                                                                        "Blog post",
                                                                    ),
                                                                    (
                                                                        "podcast",
                                                                        "Podcast",
                                                                    ),
                                                                    ("video", "Video"),
                                                                    (
                                                                        "video-external",
                                                                        "External video",
                                                                    ),
                                                                    (
                                                                        "external-link",
                                                                        "External link",
                                                                    ),
                                                                ],
                                                                label="Category",
                                                            ),
                                                        ),
                                                        (
                                                            "publication_date",
                                                            wagtail.blocks.CharBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "author",
                                                            wagtail.blocks.CharBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "duration",
                                                            wagtail.blocks.CharBlock(
                                                                help_text="Podcast or video duration.",
                                                                label="Duration",
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
                                                            "target_blank",
                                                            wagtail.blocks.BooleanBlock(
                                                                label="Should this URL open in a new tab? <p style='font-size: 11px;'>Tick the box if 'yes'</p>",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "cta_label",
                                                            wagtail.blocks.CharBlock(
                                                                help_text="The text displayed on the button for your URL. If your URL links to an external site, please add the name of the site users will land on, and what they will find on this page. For example 'Watch our short film  <strong>about Shakespeare on YouTube</strong>'.",
                                                                label="Call to action label",
                                                                max_length=50,
                                                            ),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.blocks.StructBlock(
                                                                [
                                                                    (
                                                                        "image",
                                                                        wagtail.images.blocks.ImageChooserBlock(
                                                                            required=False
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "decorative",
                                                                        wagtail.blocks.BooleanBlock(
                                                                            default=False,
                                                                            help_text='Decorative images are used for visual effect and do not add information to the content of a page. <a href="https://www.w3.org/WAI/tutorials/images/decorative/" target="_blank">"Check the guidance to see if your image is decorative</a>.',
                                                                            label="Is this image decorative? <p class='field-title__subheading'>Tick the box if 'yes'</p>",
                                                                            required=False,
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "alt_text",
                                                                        wagtail.blocks.CharBlock(
                                                                            help_text='Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. Decorative images do not require alt text. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                                                                            label="Image alternative text",
                                                                            max_length=100,
                                                                            required=False,
                                                                        ),
                                                                    ),
                                                                ],
                                                                label="Teaser image",
                                                                template="articles/blocks/images/blog-embed__image-container.html",
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
                                                            "category",
                                                            wagtail.snippets.blocks.SnippetChooserBlock(
                                                                "categories.Category"
                                                            ),
                                                        ),
                                                        (
                                                            "summary",
                                                            wagtail.blocks.RichTextBlock(
                                                                features=[
                                                                    "bold",
                                                                    "italic",
                                                                    "link",
                                                                ],
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
                                                                                help_text="The title of the target page",
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
                                                                                help_text="A description of the target page",
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
                                                "record_links",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "items",
                                                            wagtail.blocks.ListBlock(
                                                                etna.records.blocks.RecordLinkBlock,
                                                                label="Items",
                                                            ),
                                                        )
                                                    ]
                                                ),
                                            ),
                                        ],
                                        required=False,
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
