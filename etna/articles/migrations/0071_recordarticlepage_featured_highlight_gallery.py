# Generated by Django 4.1.7 on 2023-03-23 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0037_timeperiodexplorerpage_featured_record_article_and_more"),
        ("articles", "0070_alter_articlepage_mark_new_on_next_publish"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordarticlepage",
            name="featured_highlight_gallery",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="collections.highlightgallerypage",
                verbose_name="featured highlight gallery",
            ),
        ),
    ]
