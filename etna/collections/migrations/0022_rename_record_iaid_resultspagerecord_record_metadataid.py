# Generated by Django 3.2.13 on 2022-07-19 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0021_add_feature_insights"),
    ]

    operations = [
        migrations.RenameField(
            model_name="resultspagerecord",
            old_name="record_metadataId",
            new_name="record_metadataId",
        ),
    ]
