# Generated by Django 3.1.8 on 2021-07-12 09:19

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0010_timeperiodexplorerpage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="explorerindexpage",
            name="body",
            field=wagtail.fields.StreamField([], blank=True),
        ),
    ]
