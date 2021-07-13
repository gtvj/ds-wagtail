# Generated by Django 3.1.8 on 2021-07-13 13:46

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('collections', '0014_auto_20210713_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeperiodexplorerindexpage',
            name='teaser_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='topicexplorerindexpage',
            name='teaser_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='explorerindexpage',
            name='body',
            field=wagtail.core.fields.StreamField([('time_period_explorer', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(default='Explore by time period', max_length=100)), ('sub_heading', wagtail.core.blocks.CharBlock(default='Discover 1,000 years of British history through time periods including:', max_length=200)), ('page', wagtail.core.blocks.PageChooserBlock(page_type=['collections.TimePeriodExplorerIndexPage']))])), ('topic_explorer_explorer', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(default='Explore by topic', max_length=100)), ('sub_heading', wagtail.core.blocks.CharBlock(default='Browse highlights of the collection through topics including:', max_length=200)), ('page', wagtail.core.blocks.PageChooserBlock(page_type=['collections.TopicExplorerIndexPage']))]))], blank=True),
        ),
    ]
