# Generated by Django 4.0.8 on 2023-02-16 15:37

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0029_highlightgallerypage_highlight"),
    ]

    operations = [
        migrations.AddField(
            model_name="explorerindexpage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resultspage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="timeperiodexplorerindexpage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="timeperiodexplorerpage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="topicexplorerindexpage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="topicexplorerpage",
            name="teaser_text",
            field=models.TextField(
                default="",
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="highlightgallerypage",
            name="teaser_text",
            field=models.TextField(
                help_text="A short, enticing description of this page. This will appear in promos and under thumbnails around the site.",
                max_length=160,
                verbose_name="teaser text",
            ),
        ),
    ]
