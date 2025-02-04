# Generated by Django 5.1.4 on 2025-01-27 13:03
# etna:allowAlterField
# etna:allowRemoveField

import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatson', '0016_alter_exhibitionpage_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exhibitionpage',
            name='location_link_text',
        ),
        migrations.RemoveField(
            model_name='exhibitionpage',
            name='location_link_url',
        ),
        migrations.AddField(
            model_name='exhibitionpage',
            name='exhibition_highlights_title',
            field=models.CharField(blank=True, help_text="Leave blank to default to 'Exhibition highlights'.", max_length=100, verbose_name='exhibition highlights title'),
        ),
        migrations.AddField(
            model_name='exhibitionpage',
            name='intro_title',
            field=models.CharField(blank=True, help_text="Only used in jump links. Does not appear on page. Leave blank to default to 'About [Page title]'.", max_length=100, verbose_name='intro title'),
        ),
        migrations.AddField(
            model_name='exhibitionpage',
            name='location_address',
            field=wagtail.fields.RichTextField(blank=True, help_text='Leave blank to default to TNA address.', null=True, verbose_name='location address'),
        ),
        migrations.AddField(
            model_name='exhibitionpage',
            name='plan_your_visit_image',
            field=wagtail.fields.StreamField([('image', 3)], blank=True, block_lookup={0: ('etna.core.blocks.image.APIImageChooserBlock', (), {'rendition_size': 'max-900x900', 'required': True}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.', 'label': 'Alternative text', 'max_length': 100}), 2: ('etna.core.blocks.paragraph.APIRichTextBlock', (), {'features': ['bold', 'italic', 'link'], 'help_text': 'If provided, displays directly below the image. Can be used to specify sources, transcripts or other useful metadata.', 'label': 'Caption (optional)', 'required': False}), 3: ('wagtail.blocks.StructBlock', [[('image', 0), ('alt_text', 1), ('caption', 2)]], {})}, null=True),
        ),
        migrations.AddField(
            model_name='exhibitionpage',
            name='plan_your_visit_title',
            field=models.CharField(blank=True, help_text="Leave blank to default to 'Plan your visit'.", max_length=100),
        ),
        migrations.AddField(
            model_name='exhibitionpage',
            name='video_title',
            field=models.CharField(blank=True, help_text='The title of the video section.', max_length=100, verbose_name='video title'),
        ),
        migrations.AlterField(
            model_name='exhibitionpage',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='exhibitionpage',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
    ]
