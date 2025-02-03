# Generated by Django 5.1.5 on 2025-01-30 16:02
# etna:allowAlterField

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0015_peopleindexpage_short_title_personpage_short_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personpage',
            name='research_summary',
            field=wagtail.fields.StreamField([('contact', 8), ('inset_text', 10), ('paragraph', 10), ('content_section', 13)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {}), 1: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['link'], 'required': False}), 2: ('wagtail.blocks.TextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 3: ('wagtail.blocks.CharBlock', (), {'required': False}), 4: ('wagtail.blocks.URLBlock', (), {'required': False}), 5: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'required': False}), 6: ('wagtail.blocks.EmailBlock', (), {'required': False}), 7: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'required': False}), 8: ('wagtail.blocks.StructBlock', [[('title', 0), ('body', 1), ('address', 2), ('telephone', 3), ('chat_link', 4), ('chat_note', 5), ('email', 6), ('website_link', 4), ('social_media', 7)]], {}), 9: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link', 'ol', 'ul']}), 10: ('wagtail.blocks.StructBlock', [[('text', 9)]], {}), 11: ('wagtail.blocks.CharBlock', (), {'label': 'Heading', 'max_length': 100}), 12: ('wagtail.blocks.StreamBlock', [[('contact', 8), ('inset_text', 10), ('paragraph', 10)]], {'required': False}), 13: ('wagtail.blocks.StructBlock', [[('heading', 11), ('content', 12)]], {})}, null=True),
        ),
    ]
