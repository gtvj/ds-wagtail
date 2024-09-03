# Generated by Django 5.0.9 on 2024-09-03 15:10

import etna.records.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("generic_pages", "0034_alter_generalpage_page_sidebar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("accordions", 10),
                    ("button", 15),
                    ("call_to_action", 17),
                    ("contact", 23),
                    ("description_list", 27),
                    ("details", 28),
                    ("document", 6),
                    ("do_dont_list", 33),
                    ("featured_record_article", 35),
                    ("image", 39),
                    ("image_gallery", 41),
                    ("inset_text", 43),
                    ("media", 47),
                    ("paragraph", 43),
                    ("promoted_item", 59),
                    ("promoted_list", 66),
                    ("quote", 69),
                    ("record_links", 71),
                    ("table", 73),
                    ("warning_text", 74),
                    ("youtube_video", 78),
                    ("content_section", 85),
                ],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.CharBlock", (), {"required": True}),
                    1: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "link",
                                "footnotes",
                                "ol",
                                "ul",
                            ],
                            "required": True,
                        },
                    ),
                    2: ("wagtail.contrib.table_block.blocks.TableBlock", (), {}),
                    3: (
                        "wagtail.documents.blocks.DocumentChooserBlock",
                        (),
                        {"required": True},
                    ),
                    4: ("wagtail.blocks.StructBlock", [[("file", 3)]], {}),
                    5: ("wagtail.blocks.ListBlock", (4,), {}),
                    6: ("wagtail.blocks.StructBlock", [[("documents", 5)]], {}),
                    7: (
                        "wagtail.blocks.StreamBlock",
                        [[("text", 1), ("table", 2), ("documents", 6)]],
                        {},
                    ),
                    8: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 0), ("body", 7)]],
                        {},
                    ),
                    9: ("wagtail.blocks.ListBlock", (8,), {}),
                    10: ("wagtail.blocks.StructBlock", [[("items", 9)]], {}),
                    11: ("wagtail.blocks.CharBlock", (), {}),
                    12: (
                        "etna.core.blocks.page_chooser.APIPageChooserBlock",
                        (),
                        {"required": False},
                    ),
                    13: ("wagtail.blocks.URLBlock", (), {"required": False}),
                    14: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "help_text": "Use the accented button style",
                            "label": "Accented",
                            "required": False,
                        },
                    ),
                    15: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("label", 11),
                                ("link", 12),
                                ("external_link", 13),
                                ("accented", 14),
                            ]
                        ],
                        {},
                    ),
                    16: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "link",
                                "footnotes",
                                "ol",
                                "ul",
                            ],
                            "max_length": 100,
                        },
                    ),
                    17: (
                        "wagtail.blocks.StructBlock",
                        [[("body", 16), ("button", 15)]],
                        {},
                    ),
                    18: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link", "footnotes"],
                            "required": False,
                        },
                    ),
                    19: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    20: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"required": False},
                    ),
                    21: ("wagtail.blocks.EmailBlock", (), {"required": False}),
                    22: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link", "footnotes"],
                            "required": False,
                        },
                    ),
                    23: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 11),
                                ("address", 18),
                                ("telephone", 19),
                                ("chat_link", 13),
                                ("chat_note", 20),
                                ("email", 21),
                                ("website_link", 13),
                                ("social_media", 22),
                            ]
                        ],
                        {},
                    ),
                    24: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {"features": ["bold", "italic", "link", "footnotes"]},
                    ),
                    25: (
                        "wagtail.blocks.StructBlock",
                        [[("term", 0), ("detail", 24)]],
                        {},
                    ),
                    26: ("wagtail.blocks.ListBlock", (25,), {}),
                    27: ("wagtail.blocks.StructBlock", [[("items", 26)]], {}),
                    28: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 0), ("body", 1)]],
                        {},
                    ),
                    29: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 24)]],
                        {"icon": "check", "label": "Do item"},
                    ),
                    30: ("wagtail.blocks.ListBlock", (29,), {"label": "Dos"}),
                    31: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 24)]],
                        {"icon": "cross", "label": "Don't item"},
                    ),
                    32: ("wagtail.blocks.ListBlock", (31,), {"label": "Don'ts"}),
                    33: (
                        "wagtail.blocks.StructBlock",
                        [[("do", 30), ("dont", 32)]],
                        {},
                    ),
                    34: (
                        "etna.core.blocks.page_chooser.APIPageChooserBlock",
                        (),
                        {
                            "label": "Page",
                            "page_type": ["articles.RecordArticlePage"],
                            "required_api_fields": ["teaser_image"],
                        },
                    ),
                    35: ("wagtail.blocks.StructBlock", [[("page", 34)]], {}),
                    36: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {"rendition_size": "max-900x900", "required": True},
                    ),
                    37: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                            "label": "Alternative text",
                            "max_length": 100,
                        },
                    ),
                    38: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link"],
                            "help_text": "If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.",
                            "label": "Caption (optional)",
                            "required": False,
                        },
                    ),
                    39: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 36), ("alt_text", 37), ("caption", 38)]],
                        {},
                    ),
                    40: ("wagtail.blocks.ListBlock", (39,), {}),
                    41: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 19), ("description", 22), ("images", 40)]],
                        {},
                    ),
                    42: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "link",
                                "footnotes",
                                "ol",
                                "ul",
                            ]
                        },
                    ),
                    43: ("wagtail.blocks.StructBlock", [[("text", 42)]], {}),
                    44: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "A descriptive title for the media block",
                            "required": True,
                        },
                    ),
                    45: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {"help_text": "A background image for the media block"},
                    ),
                    46: ("etna.media.blocks.MediaChooserBlock", (), {}),
                    47: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 44), ("background_image", 45), ("media", 46)]],
                        {},
                    ),
                    48: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Title of the promoted page",
                            "label": "Title",
                            "max_length": 100,
                        },
                    ),
                    49: (
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
                    50: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "This is a free text field. Please enter date as per agreed format: 14 April 2021",
                            "required": False,
                        },
                    ),
                    51: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Podcast or video duration.",
                            "label": "Duration",
                            "max_length": 50,
                            "required": False,
                        },
                    ),
                    52: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {
                            "help_text": "URL for the external page",
                            "label": "External URL",
                        },
                    ),
                    53: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "label": "Should this URL open in a new tab? <p style='font-size: 11px;'>Tick the box if 'yes'</p>",
                            "required": False,
                        },
                    ),
                    54: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "The text displayed on the button for your URL. If your URL links to an external site, please add the name of the site users will land on, and what they will find on this page. For example 'Watch our short film  <strong>about Shakespeare on YouTube</strong>'.",
                            "label": "Call to action label",
                            "max_length": 50,
                        },
                    ),
                    55: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": False,
                            "help_text": 'Decorative images are used for visual effect and do not add information to the content of a page. <a href="https://www.w3.org/WAI/tutorials/images/decorative/" target="_blank">"Check the guidance to see if your image is decorative</a>.',
                            "label": "Is this image decorative? <p class='field-title__subheading'>Tick the box if 'yes'</p>",
                            "required": False,
                        },
                    ),
                    56: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. Decorative images do not require alt text. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                            "label": "Image alternative text",
                            "max_length": 100,
                            "required": False,
                        },
                    ),
                    57: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 36), ("decorative", 55), ("alt_text", 56)]],
                        {
                            "label": "Teaser image",
                            "template": "articles/blocks/images/blog-embed__image-container.html",
                        },
                    ),
                    58: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link", "footnotes"],
                            "help_text": "A description of the promoted page",
                        },
                    ),
                    59: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 48),
                                ("category", 49),
                                ("publication_date", 50),
                                ("author", 19),
                                ("duration", 51),
                                ("url", 52),
                                ("target_blank", 53),
                                ("cta_label", 54),
                                ("image", 57),
                                ("description", 58),
                            ]
                        ],
                        {},
                    ),
                    60: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("categories.Category",),
                        {},
                    ),
                    61: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "The title of the target page",
                            "max_length": 100,
                            "required": True,
                        },
                    ),
                    62: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link", "footnotes"],
                            "help_text": "A description of the target page",
                            "required": False,
                        },
                    ),
                    63: ("wagtail.blocks.URLBlock", (), {"required": True}),
                    64: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 61), ("description", 62), ("url", 63)]],
                        {},
                    ),
                    65: ("wagtail.blocks.ListBlock", (64,), {}),
                    66: (
                        "wagtail.blocks.StructBlock",
                        [[("category", 60), ("summary", 22), ("promoted_items", 65)]],
                        {},
                    ),
                    67: (
                        "etna.core.blocks.paragraph.APIRichTextBlock",
                        (),
                        {
                            "features": ["bold", "italic", "link", "footnotes"],
                            "required": True,
                        },
                    ),
                    68: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 100, "required": False},
                    ),
                    69: (
                        "wagtail.blocks.StructBlock",
                        [[("quote", 67), ("attribution", 68)]],
                        {},
                    ),
                    70: (
                        "wagtail.blocks.ListBlock",
                        (etna.records.blocks.RecordLinkBlock,),
                        {"label": "Items"},
                    ),
                    71: ("wagtail.blocks.StructBlock", [[("items", 70)]], {}),
                    72: (
                        "wagtail.contrib.table_block.blocks.TableBlock",
                        (),
                        {
                            "table_options": {
                                "contextMenu": [
                                    "row_above",
                                    "row_below",
                                    "---------",
                                    "col_left",
                                    "col_right",
                                    "---------",
                                    "remove_row",
                                    "remove_col",
                                    "---------",
                                    "undo",
                                    "redo",
                                    "---------",
                                    "alignment",
                                ]
                            }
                        },
                    ),
                    73: ("wagtail.blocks.StructBlock", [[("table", 72)]], {}),
                    74: ("wagtail.blocks.StructBlock", [[("body", 42)]], {}),
                    75: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Title", "max_length": 100, "required": True},
                    ),
                    76: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "label": "YouTube Video ID",
                            "max_length": 11,
                            "required": True,
                        },
                    ),
                    77: (
                        "etna.core.blocks.image.APIImageChooserBlock",
                        (),
                        {
                            "label": "Preview Image",
                            "rendition_size": "max-640x360",
                            "required": False,
                        },
                    ),
                    78: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 75), ("video_id", 76), ("preview_image", 77)]],
                        {},
                    ),
                    79: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Heading", "max_length": 100},
                    ),
                    80: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Sub-heading", "max_length": 100},
                    ),
                    81: ("wagtail.blocks.StructBlock", [[("heading", 80)]], {}),
                    82: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Sub-sub-heading", "max_length": 100},
                    ),
                    83: ("wagtail.blocks.StructBlock", [[("heading", 82)]], {}),
                    84: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("accordions", 10),
                                ("button", 15),
                                ("call_to_action", 17),
                                ("contact", 23),
                                ("description_list", 27),
                                ("details", 28),
                                ("document", 6),
                                ("do_dont_list", 33),
                                ("featured_record_article", 35),
                                ("image", 39),
                                ("image_gallery", 41),
                                ("inset_text", 43),
                                ("media", 47),
                                ("paragraph", 43),
                                ("promoted_item", 59),
                                ("promoted_list", 66),
                                ("quote", 69),
                                ("record_links", 71),
                                ("sub_heading", 81),
                                ("sub_sub_heading", 83),
                                ("table", 73),
                                ("warning_text", 74),
                                ("youtube_video", 78),
                            ]
                        ],
                        {"required": False},
                    ),
                    85: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 79), ("content", 84)]],
                        {},
                    ),
                },
                null=True,
            ),
        ),
    ]
