# Generated by Django 4.0.8 on 2022-11-04 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0023_add_search_image_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="timeperiodexplorerindexpage",
            name="sub_heading",
        ),
        migrations.RemoveField(
            model_name="timeperiodexplorerpage",
            name="sub_heading",
        ),
        migrations.RemoveField(
            model_name="topicexplorerindexpage",
            name="sub_heading",
        ),
        migrations.RemoveField(
            model_name="topicexplorerpage",
            name="sub_heading",
        ),
    ]