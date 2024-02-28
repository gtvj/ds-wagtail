# Generated by Django 4.0.8 on 2023-03-10 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0005_alter_customimage_file_and_more"),
        ("collections", "0033_set_teaser_text_from_intro"),
    ]

    operations = [
        migrations.AlterField(
            model_name="explorerindexpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="highlightgallerypage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="resultspage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="resultspagerecord",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerindexpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerindexpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear on thumbnails and promos around the site.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
    ]
