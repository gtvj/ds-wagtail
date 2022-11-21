# Generated by Django 4.0.8 on 2022-11-17 17:10

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('collections', '0023_add_search_image_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explorerindexpage',
            name='body',
            field=wagtail.fields.StreamField([('time_period_explorer_index', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(default='Explore by time period', max_length=100)), ('page', wagtail.blocks.PageChooserBlock(page_type=['collections.TimePeriodExplorerIndexPage']))])), ('topic_explorer_index', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(default='Explore by topic', max_length=100)), ('page', wagtail.blocks.PageChooserBlock(page_type=['collections.TopicExplorerIndexPage']))]))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='timeperiodexplorerindexpage',
            name='body',
            field=wagtail.fields.StreamField([('topic_explorer_index', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(default='Explore by topic', max_length=100)), ('page', wagtail.blocks.PageChooserBlock(page_type=['collections.TopicExplorerIndexPage']))]))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='topicexplorerindexpage',
            name='body',
            field=wagtail.fields.StreamField([('time_period_explorer_index', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(default='Explore by time period', max_length=100)), ('page', wagtail.blocks.PageChooserBlock(page_type=['collections.TimePeriodExplorerIndexPage']))]))], blank=True, use_json_field=True),
        ),
    ]
