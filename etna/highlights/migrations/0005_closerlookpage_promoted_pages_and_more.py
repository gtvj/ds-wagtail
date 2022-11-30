# Generated by Django 4.0.8 on 2022-11-30 11:53

from django.db import migrations, models
import etna.highlights.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('highlights', '0004_alter_closerlookpage_standfirst_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='closerlookpage',
            name='promoted_pages',
            field=wagtail.fields.StreamField([('promoted_pages', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(max_length=100)), ('promoted_items', wagtail.blocks.ListBlock(etna.highlights.blocks.PromotedItemBlock, max=3, min=1))]))], null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='closerlookgalleryimage',
            name='caption',
            field=models.CharField(blank=True, help_text='A caption for the image', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='closerlookgalleryimage',
            name='transcription_text',
            field=models.TextField(blank=True, help_text='A transcription of the image', max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='closerlookgalleryimage',
            name='translation_text',
            field=models.TextField(blank=True, help_text='A translation of the transcription', max_length=800, null=True),
        ),
    ]
