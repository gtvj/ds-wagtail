# Generated by Django 4.0.8 on 2022-12-16 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0077_alter_revision_user'),
        ('wagtailimages', '0024_index_image_file_hash'),
        ('insights', '0047_rename_insightspage_storiespage_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InsightsIndexPage',
            new_name='StoriesIndexPage',
        ),
    ]
