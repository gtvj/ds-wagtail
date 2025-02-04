# Generated by Django 5.1.5 on 2025-01-30 16:02
# etna:allowAlterField

import django.core.validators
import etna.records.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blogindexpage_short_title_blogpage_short_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.fields.StreamField([('call_to_action', 6), ('contact', 13), ('document', 17), ('featured_external_link', 22), ('featured_page', 25), ('image', 29), ('image_gallery', 31), ('inset_text', 33), ('media', 37), ('paragraph', 33), ('quote', 40), ('record', 42), ('table', 44), ('youtube_video', 50), ('content_section', 55)], block_lookup={0: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul'], 'max_length': 100}), 1: ('wagtail.blocks.CharBlock', (), {}), 2: ('etna.core.blocks.page_chooser.APIPageChooserBlock', (), {'required': False}), 3: ('wagtail.blocks.URLBlock', (), {'required': False}), 4: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Use the accented button style', 'label': 'Accented', 'required': False}), 5: ('wagtail.blocks.StructBlock', [[('label', 1), ('link', 2), ('external_link', 3), ('accented', 4)]], {}), 6: ('wagtail.blocks.StructBlock', [[('body', 0), ('button', 5)]], {}), 7: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['link'], 'required': False}), 8: ('wagtail.blocks.TextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 9: ('wagtail.blocks.CharBlock', (), {'required': False}), 10: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'required': False}), 11: ('wagtail.blocks.EmailBlock', (), {'required': False}), 12: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 13: ('wagtail.blocks.StructBlock', [[('title', 1), ('body', 7), ('address', 8), ('telephone', 9), ('chat_link', 3), ('chat_note', 10), ('email', 11), ('website_link', 3), ('social_media', 12)]], {}), 14: ('wagtail.documents.blocks.DocumentChooserBlock', (), {'required': True}), 15: ('wagtail.blocks.StructBlock', [[('file', 14)]], {}), 16: ('wagtail.blocks.ListBlock', (15,), {}), 17: ('wagtail.blocks.StructBlock', [[('documents', 16)]], {}), 18: ('wagtail.blocks.CharBlock', (), {'label': 'Title', 'max_length': 100}), 19: ('wagtail.blocks.CharBlock', (), {'label': 'Description'}), 20: ('wagtail.blocks.URLBlock', (), {'label': 'URL'}), 21: ('etna.core.blocks.image.APIImageChooserBlock', (), {'label': 'Image', 'required': False}), 22: ('wagtail.blocks.StructBlock', [[('title', 18), ('description', 19), ('url', 20), ('image', 21)]], {}), 23: ('etna.core.blocks.page_chooser.APIPageChooserBlock', (), {'label': 'Page', 'page_type': ['wagtailcore.Page'], 'required': True}), 24: ('wagtail.blocks.CharBlock', (), {'help_text': 'Optional override for the teaser text', 'label': 'Teaser text override', 'required': False}), 25: ('wagtail.blocks.StructBlock', [[('page', 23), ('teaser_text', 24)]], {}), 26: ('etna.core.blocks.image.APIImageChooserBlock', (), {'rendition_size': 'max-900x900', 'required': True}), 27: ('wagtail.blocks.CharBlock', (), {'help_text': 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.', 'label': 'Alternative text', 'max_length': 100}), 28: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'help_text': 'If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.', 'label': 'Caption (optional)', 'required': False}), 29: ('wagtail.blocks.StructBlock', [[('image', 26), ('alt_text', 27), ('caption', 28)]], {}), 30: ('wagtail.blocks.ListBlock', (29,), {}), 31: ('wagtail.blocks.StructBlock', [[('title', 9), ('description', 12), ('images', 30)]], {}), 32: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul']}), 33: ('wagtail.blocks.StructBlock', [[('text', 32)]], {}), 34: ('wagtail.blocks.CharBlock', (), {'help_text': 'A descriptive title for the media block', 'required': True}), 35: ('etna.core.blocks.image.APIImageChooserBlock', (), {'help_text': 'A thumbnail image for the media block', 'required': False}), 36: ('etna.media.blocks.MediaChooserBlock', (), {}), 37: ('wagtail.blocks.StructBlock', [[('title', 34), ('thumbnail', 35), ('media', 36)]], {}), 38: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul'], 'required': True}), 39: ('wagtail.blocks.CharBlock', (), {'max_length': 100, 'required': False}), 40: ('wagtail.blocks.StructBlock', [[('quote', 38), ('attribution', 39)]], {}), 41: ('wagtail.blocks.ListBlock', (etna.records.blocks.RecordLinkBlock,), {'label': 'Items'}), 42: ('wagtail.blocks.StructBlock', [[('items', 41)]], {}), 43: ('wagtail.contrib.table_block.blocks.TableBlock', (), {'table_options': {'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'alignment']}}), 44: ('wagtail.blocks.StructBlock', [[('table', 43)]], {}), 45: ('wagtail.blocks.CharBlock', (), {'label': 'Title', 'max_length': 100, 'required': True}), 46: ('wagtail.blocks.CharBlock', (), {'label': 'YouTube Video ID', 'max_length': 11, 'required': True, 'validators': [django.core.validators.RegexValidator(message='Invalid YouTube Video ID', regex='^[a-zA-Z0-9_-]{11}$')]}), 47: ('etna.core.blocks.image.APIImageChooserBlock', (), {'label': 'Preview Image', 'rendition_size': 'fill-640x360', 'required': True}), 48: ('wagtail.blocks.RichTextBlock', (), {'label': 'Transcript', 'required': False}), 49: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Tick if the video has captions on YouTube', 'label': 'Captions available', 'required': False}), 50: ('wagtail.blocks.StructBlock', [[('title', 45), ('video_id', 46), ('preview_image', 47), ('transcript', 48), ('captions_available', 49)]], {}), 51: ('wagtail.blocks.CharBlock', (), {'label': 'Heading', 'max_length': 100}), 52: ('wagtail.blocks.CharBlock', (), {'label': 'Sub-heading', 'max_length': 100}), 53: ('wagtail.blocks.StructBlock', [[('heading', 52)]], {}), 54: ('wagtail.blocks.StreamBlock', [[('call_to_action', 6), ('contact', 13), ('document', 17), ('featured_external_link', 22), ('featured_page', 25), ('image', 29), ('image_gallery', 31), ('inset_text', 33), ('media', 37), ('paragraph', 33), ('quote', 40), ('record', 42), ('sub_heading', 53), ('table', 44), ('youtube_video', 50)]], {'required': False}), 55: ('wagtail.blocks.StructBlock', [[('heading', 51), ('content', 54)]], {})}),
        ),
    ]
