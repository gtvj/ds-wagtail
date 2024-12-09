# Generated by Django 5.1.2 on 2024-11-27 17:27
# etna:allowAlterField

import etna.records.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "articles",
            "0111_remove_articleindexpage_uuid_remove_articlepage_uuid_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlepage",
            name="body",
            field=wagtail.fields.StreamField(
                [("content_section", 50)],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Heading", "max_length": 100},
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Title", "max_length": 100},
                    ),
                    2: ("wagtail.blocks.CharBlock", (), {"label": "Description"}),
                    3: ("wagtail.blocks.URLBlock", (), {"label": "URL"}),
                    4: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {"label": "Image", "required": False},
                    ),
                    5: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 1), ("description", 2), ("url", 3), ("image", 4)]],
                        {},
                    ),
                    6: (
                        "etna.core.blocks.page_chooser.APIPageChooserBlock",
                        (),
                        {
                            "label": "Page",
                            "page_type": ["wagtailcore.Page"],
                            "required": True,
                        },
                    ),
                    7: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Optional override for the teaser text",
                            "label": "Teaser text override",
                            "required": False,
                        },
                    ),
                    8: (
                        "wagtail.blocks.StructBlock",
                        [[("page", 6), ("teaser_text", 7)]],
                        {},
                    ),
                    9: (
                        "etna.core.blocks.page_chooser.APIPageChooserBlock",
                        (),
                        {
                            "label": "Page",
                            "page_type": ["articles.RecordArticlePage"],
                            "required_api_fields": ["teaser_image"],
                        },
                    ),
                    10: ("wagtail.blocks.StructBlock", [[("page", 9)]], {}),
                    11: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {"rendition_size": "max-900x900", "required": True},
                    ),
                    12: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                            "label": "Alternative text",
                            "max_length": 100,
                        },
                    ),
                    13: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.",
                            "label": "Caption (optional)",
                            "required": False,
                        },
                    ),
                    14: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 11), ("alt_text", 12), ("caption", 13)]],
                        {},
                    ),
                    15: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "A descriptive title for the media block",
                            "required": True,
                        },
                    ),
                    16: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {
                            "help_text": "A thumbnail image for the media block",
                            "required": False,
                        },
                    ),
                    17: ("etna.media.blocks.MediaChooserBlock", (), {}),
                    18: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 15), ("thumbnail", 16), ("media", 17)]],
                        {},
                    ),
                    19: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link", "ol", "ul"]},
                    ),
                    20: ("wagtail.blocks.StructBlock", [[("text", 19)]], {}),
                    21: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Title of the promoted page",
                            "label": "Title",
                            "max_length": 100,
                        },
                    ),
                    22: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("blog", "Blog post"),
                                ("podcast", "Podcast"),
                                ("video", "Video"),
                                ("video-external", "External video"),
                                ("external-link", "External link"),
                            ],
                            "label": "Category",
                        },
                    ),
                    23: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "This is a free text field. Please enter date as per agreed format: 14 April 2021",
                            "required": False,
                        },
                    ),
                    24: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    25: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Podcast or video duration.",
                            "label": "Duration",
                            "max_length": 50,
                            "required": False,
                        },
                    ),
                    26: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {
                            "help_text": "URL for the external page",
                            "label": "External URL",
                        },
                    ),
                    27: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "label": "Should this URL open in a new tab? <p style='font-size: 11px;'>Tick the box if 'yes'</p>",
                            "required": False,
                        },
                    ),
                    28: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "The text displayed on the button for your URL. If your URL links to an external site, please add the name of the site users will land on, and what they will find on this page. For example 'Watch our short film  <strong>about Shakespeare on YouTube</strong>'.",
                            "label": "Call to action label",
                            "max_length": 50,
                        },
                    ),
                    29: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": False,
                            "help_text": 'Decorative images are used for visual effect and do not add information to the content of a page. <a href="https://www.w3.org/WAI/tutorials/images/decorative/" target="_blank">"Check the guidance to see if your image is decorative</a>.',
                            "label": "Is this image decorative? <p class='field-title__subheading'>Tick the box if 'yes'</p>",
                            "required": False,
                        },
                    ),
                    30: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. Decorative images do not require alt text. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                            "label": "Image alternative text",
                            "max_length": 100,
                            "required": False,
                        },
                    ),
                    31: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 11), ("decorative", 29), ("alt_text", 30)]],
                        {
                            "label": "Teaser image",
                            "template": "articles/blocks/images/blog-embed__image-container.html",
                        },
                    ),
                    32: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "A description of the promoted page",
                        },
                    ),
                    33: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 21),
                                ("category", 22),
                                ("publication_date", 23),
                                ("author", 24),
                                ("duration", 25),
                                ("url", 26),
                                ("target_blank", 27),
                                ("cta_label", 28),
                                ("image", 31),
                                ("description", 32),
                            ]
                        ],
                        {},
                    ),
                    34: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("categories.Category",),
                        {},
                    ),
                    35: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link"], "required": False},
                    ),
                    36: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "The title of the target page",
                            "max_length": 100,
                            "required": True,
                        },
                    ),
                    37: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "A description of the target page",
                            "required": False,
                        },
                    ),
                    38: ("wagtail.blocks.URLBlock", (), {"required": True}),
                    39: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 36), ("description", 37), ("url", 38)]],
                        {},
                    ),
                    40: ("wagtail.blocks.ListBlock", (39,), {}),
                    41: (
                        "wagtail.blocks.StructBlock",
                        [[("category", 34), ("summary", 35), ("promoted_items", 40)]],
                        {},
                    ),
                    42: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link"], "required": True},
                    ),
                    43: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 100, "required": False},
                    ),
                    44: (
                        "wagtail.blocks.StructBlock",
                        [[("quote", 42), ("attribution", 43)]],
                        {},
                    ),
                    45: (
                        "wagtail.blocks.ListBlock",
                        (etna.records.blocks.RecordLinkBlock,),
                        {"label": "Items"},
                    ),
                    46: ("wagtail.blocks.StructBlock", [[("items", 45)]], {}),
                    47: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Sub-heading", "max_length": 100},
                    ),
                    48: ("wagtail.blocks.StructBlock", [[("heading", 47)]], {}),
                    49: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("featured_external_link", 5),
                                ("featured_page", 8),
                                ("featured_record_article", 10),
                                ("image", 14),
                                ("media", 18),
                                ("paragraph", 20),
                                ("promoted_item", 33),
                                ("promoted_list", 41),
                                ("quote", 44),
                                ("record_links", 46),
                                ("sub_heading", 48),
                            ]
                        ],
                        {"required": False},
                    ),
                    50: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 0), ("content", 49)]],
                        {},
                    ),
                },
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="focusedarticlepage",
            name="body",
            field=wagtail.fields.StreamField(
                [("content_section", 50)],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Heading", "max_length": 100},
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Title", "max_length": 100},
                    ),
                    2: ("wagtail.blocks.CharBlock", (), {"label": "Description"}),
                    3: ("wagtail.blocks.URLBlock", (), {"label": "URL"}),
                    4: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {"label": "Image", "required": False},
                    ),
                    5: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 1), ("description", 2), ("url", 3), ("image", 4)]],
                        {},
                    ),
                    6: (
                        "etna.core.blocks.page_chooser.APIPageChooserBlock",
                        (),
                        {
                            "label": "Page",
                            "page_type": ["wagtailcore.Page"],
                            "required": True,
                        },
                    ),
                    7: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Optional override for the teaser text",
                            "label": "Teaser text override",
                            "required": False,
                        },
                    ),
                    8: (
                        "wagtail.blocks.StructBlock",
                        [[("page", 6), ("teaser_text", 7)]],
                        {},
                    ),
                    9: (
                        "etna.core.blocks.page_chooser.APIPageChooserBlock",
                        (),
                        {
                            "label": "Page",
                            "page_type": ["articles.RecordArticlePage"],
                            "required_api_fields": ["teaser_image"],
                        },
                    ),
                    10: ("wagtail.blocks.StructBlock", [[("page", 9)]], {}),
                    11: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {"rendition_size": "max-900x900", "required": True},
                    ),
                    12: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                            "label": "Alternative text",
                            "max_length": 100,
                        },
                    ),
                    13: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.",
                            "label": "Caption (optional)",
                            "required": False,
                        },
                    ),
                    14: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 11), ("alt_text", 12), ("caption", 13)]],
                        {},
                    ),
                    15: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "A descriptive title for the media block",
                            "required": True,
                        },
                    ),
                    16: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {
                            "help_text": "A thumbnail image for the media block",
                            "required": False,
                        },
                    ),
                    17: ("etna.media.blocks.MediaChooserBlock", (), {}),
                    18: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 15), ("thumbnail", 16), ("media", 17)]],
                        {},
                    ),
                    19: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link", "ol", "ul"]},
                    ),
                    20: ("wagtail.blocks.StructBlock", [[("text", 19)]], {}),
                    21: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Title of the promoted page",
                            "label": "Title",
                            "max_length": 100,
                        },
                    ),
                    22: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("blog", "Blog post"),
                                ("podcast", "Podcast"),
                                ("video", "Video"),
                                ("video-external", "External video"),
                                ("external-link", "External link"),
                            ],
                            "label": "Category",
                        },
                    ),
                    23: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "This is a free text field. Please enter date as per agreed format: 14 April 2021",
                            "required": False,
                        },
                    ),
                    24: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    25: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Podcast or video duration.",
                            "label": "Duration",
                            "max_length": 50,
                            "required": False,
                        },
                    ),
                    26: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {
                            "help_text": "URL for the external page",
                            "label": "External URL",
                        },
                    ),
                    27: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "label": "Should this URL open in a new tab? <p style='font-size: 11px;'>Tick the box if 'yes'</p>",
                            "required": False,
                        },
                    ),
                    28: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "The text displayed on the button for your URL. If your URL links to an external site, please add the name of the site users will land on, and what they will find on this page. For example 'Watch our short film  <strong>about Shakespeare on YouTube</strong>'.",
                            "label": "Call to action label",
                            "max_length": 50,
                        },
                    ),
                    29: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": False,
                            "help_text": 'Decorative images are used for visual effect and do not add information to the content of a page. <a href="https://www.w3.org/WAI/tutorials/images/decorative/" target="_blank">"Check the guidance to see if your image is decorative</a>.',
                            "label": "Is this image decorative? <p class='field-title__subheading'>Tick the box if 'yes'</p>",
                            "required": False,
                        },
                    ),
                    30: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. Decorative images do not require alt text. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                            "label": "Image alternative text",
                            "max_length": 100,
                            "required": False,
                        },
                    ),
                    31: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 11), ("decorative", 29), ("alt_text", 30)]],
                        {
                            "label": "Teaser image",
                            "template": "articles/blocks/images/blog-embed__image-container.html",
                        },
                    ),
                    32: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "A description of the promoted page",
                        },
                    ),
                    33: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 21),
                                ("category", 22),
                                ("publication_date", 23),
                                ("author", 24),
                                ("duration", 25),
                                ("url", 26),
                                ("target_blank", 27),
                                ("cta_label", 28),
                                ("image", 31),
                                ("description", 32),
                            ]
                        ],
                        {},
                    ),
                    34: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("categories.Category",),
                        {},
                    ),
                    35: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link"], "required": False},
                    ),
                    36: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "The title of the target page",
                            "max_length": 100,
                            "required": True,
                        },
                    ),
                    37: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "A description of the target page",
                            "required": False,
                        },
                    ),
                    38: ("wagtail.blocks.URLBlock", (), {"required": True}),
                    39: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 36), ("description", 37), ("url", 38)]],
                        {},
                    ),
                    40: ("wagtail.blocks.ListBlock", (39,), {}),
                    41: (
                        "wagtail.blocks.StructBlock",
                        [[("category", 34), ("summary", 35), ("promoted_items", 40)]],
                        {},
                    ),
                    42: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link"], "required": True},
                    ),
                    43: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 100, "required": False},
                    ),
                    44: (
                        "wagtail.blocks.StructBlock",
                        [[("quote", 42), ("attribution", 43)]],
                        {},
                    ),
                    45: (
                        "wagtail.blocks.ListBlock",
                        (etna.records.blocks.RecordLinkBlock,),
                        {"label": "Items"},
                    ),
                    46: ("wagtail.blocks.StructBlock", [[("items", 45)]], {}),
                    47: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Sub-heading", "max_length": 100},
                    ),
                    48: ("wagtail.blocks.StructBlock", [[("heading", 47)]], {}),
                    49: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("featured_external_link", 5),
                                ("featured_page", 8),
                                ("featured_record_article", 10),
                                ("image", 14),
                                ("media", 18),
                                ("paragraph", 20),
                                ("promoted_item", 33),
                                ("promoted_list", 41),
                                ("quote", 44),
                                ("record_links", 46),
                                ("sub_heading", 48),
                            ]
                        ],
                        {"required": False},
                    ),
                    50: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 0), ("content", 49)]],
                        {},
                    ),
                },
                null=True,
            ),
        ),
    ]
