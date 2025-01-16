# Generated by Django 5.1.4 on 2025-01-16 15:52

import django.core.validators
import etna.records.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_blogpostpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.fields.StreamField([('call_to_action', 6), ('contact', 12), ('document', 16), ('featured_external_link', 21), ('featured_page', 24), ('image', 28), ('image_gallery', 30), ('inset_text', 32), ('media', 36), ('paragraph', 32), ('quote', 39), ('record', 41), ('table', 43), ('youtube_video', 49), ('content_section', 54)], block_lookup={0: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul'], 'max_length': 100}), 1: ('wagtail.blocks.CharBlock', (), {}), 2: ('etna.core.blocks.page_chooser.APIPageChooserBlock', (), {'required': False}), 3: ('wagtail.blocks.URLBlock', (), {'required': False}), 4: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Use the accented button style', 'label': 'Accented', 'required': False}), 5: ('wagtail.blocks.StructBlock', [[('label', 1), ('link', 2), ('external_link', 3), ('accented', 4)]], {}), 6: ('wagtail.blocks.StructBlock', [[('body', 0), ('button', 5)]], {}), 7: ('wagtail.blocks.TextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 8: ('wagtail.blocks.CharBlock', (), {'required': False}), 9: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'required': False}), 10: ('wagtail.blocks.EmailBlock', (), {'required': False}), 11: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 12: ('wagtail.blocks.StructBlock', [[('title', 1), ('address', 7), ('telephone', 8), ('chat_link', 3), ('chat_note', 9), ('email', 10), ('website_link', 3), ('social_media', 11)]], {}), 13: ('wagtail.documents.blocks.DocumentChooserBlock', (), {'required': True}), 14: ('wagtail.blocks.StructBlock', [[('file', 13)]], {}), 15: ('wagtail.blocks.ListBlock', (14,), {}), 16: ('wagtail.blocks.StructBlock', [[('documents', 15)]], {}), 17: ('wagtail.blocks.CharBlock', (), {'label': 'Title', 'max_length': 100}), 18: ('wagtail.blocks.CharBlock', (), {'label': 'Description'}), 19: ('wagtail.blocks.URLBlock', (), {'label': 'URL'}), 20: ('etna.core.blocks.image.APIImageChooserBlock', (), {'label': 'Image', 'required': False}), 21: ('wagtail.blocks.StructBlock', [[('title', 17), ('description', 18), ('url', 19), ('image', 20)]], {}), 22: ('etna.core.blocks.page_chooser.APIPageChooserBlock', (), {'label': 'Page', 'page_type': ['wagtailcore.Page'], 'required': True}), 23: ('wagtail.blocks.CharBlock', (), {'help_text': 'Optional override for the teaser text', 'label': 'Teaser text override', 'required': False}), 24: ('wagtail.blocks.StructBlock', [[('page', 22), ('teaser_text', 23)]], {}), 25: ('etna.core.blocks.image.APIImageChooserBlock', (), {'rendition_size': 'max-900x900', 'required': True}), 26: ('wagtail.blocks.CharBlock', (), {'help_text': 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.', 'label': 'Alternative text', 'max_length': 100}), 27: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'help_text': 'If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.', 'label': 'Caption (optional)', 'required': False}), 28: ('wagtail.blocks.StructBlock', [[('image', 25), ('alt_text', 26), ('caption', 27)]], {}), 29: ('wagtail.blocks.ListBlock', (28,), {}), 30: ('wagtail.blocks.StructBlock', [[('title', 8), ('description', 11), ('images', 29)]], {}), 31: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul']}), 32: ('wagtail.blocks.StructBlock', [[('text', 31)]], {}), 33: ('wagtail.blocks.CharBlock', (), {'help_text': 'A descriptive title for the media block', 'required': True}), 34: ('etna.core.blocks.image.APIImageChooserBlock', (), {'help_text': 'A thumbnail image for the media block', 'required': False}), 35: ('etna.media.blocks.MediaChooserBlock', (), {}), 36: ('wagtail.blocks.StructBlock', [[('title', 33), ('thumbnail', 34), ('media', 35)]], {}), 37: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul'], 'required': True}), 38: ('wagtail.blocks.CharBlock', (), {'max_length': 100, 'required': False}), 39: ('wagtail.blocks.StructBlock', [[('quote', 37), ('attribution', 38)]], {}), 40: ('wagtail.blocks.ListBlock', (etna.records.blocks.RecordLinkBlock,), {'label': 'Items'}), 41: ('wagtail.blocks.StructBlock', [[('items', 40)]], {}), 42: ('wagtail.contrib.table_block.blocks.TableBlock', (), {'table_options': {'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'alignment']}}), 43: ('wagtail.blocks.StructBlock', [[('table', 42)]], {}), 44: ('wagtail.blocks.CharBlock', (), {'label': 'Title', 'max_length': 100, 'required': True}), 45: ('wagtail.blocks.CharBlock', (), {'label': 'YouTube Video ID', 'max_length': 11, 'required': True, 'validators': [django.core.validators.RegexValidator(message='Invalid YouTube Video ID', regex='^[a-zA-Z0-9_-]{11}$')]}), 46: ('etna.core.blocks.image.APIImageChooserBlock', (), {'label': 'Preview Image', 'rendition_size': 'fill-640x360', 'required': True}), 47: ('wagtail.blocks.RichTextBlock', (), {'label': 'Transcript', 'required': False}), 48: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Tick if the video has captions on YouTube', 'label': 'Captions available', 'required': False}), 49: ('wagtail.blocks.StructBlock', [[('title', 44), ('video_id', 45), ('preview_image', 46), ('transcript', 47), ('captions_available', 48)]], {}), 50: ('wagtail.blocks.CharBlock', (), {'label': 'Heading', 'max_length': 100}), 51: ('wagtail.blocks.CharBlock', (), {'label': 'Sub-heading', 'max_length': 100}), 52: ('wagtail.blocks.StructBlock', [[('heading', 51)]], {}), 53: ('wagtail.blocks.StreamBlock', [[('call_to_action', 6), ('contact', 12), ('document', 16), ('featured_external_link', 21), ('featured_page', 24), ('image', 28), ('image_gallery', 30), ('inset_text', 32), ('media', 36), ('paragraph', 32), ('quote', 39), ('record', 41), ('sub_heading', 52), ('table', 43), ('youtube_video', 49)]], {'required': False}), 54: ('wagtail.blocks.StructBlock', [[('heading', 50), ('content', 53)]], {})}),
        ),
    ]
