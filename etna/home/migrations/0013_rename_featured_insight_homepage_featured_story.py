# Generated by Django 4.0.8 on 2022-11-03 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0012_homepage_featured_collections_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="homepage",
            old_name="featured_insight",
            new_name="featured_story",
        ),
    ]
