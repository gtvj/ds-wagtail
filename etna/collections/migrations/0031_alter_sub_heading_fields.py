# Generated by Django 4.0.8 on 2023-02-16 15:59

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0030_add_teaser_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="explorerindexpage",
            name="sub_heading",
            field=wagtail.fields.RichTextField(
                help_text="1-2 sentences introducing the subject of the page, and explaining why a user should read on.",
                max_length=300,
                verbose_name="introductory text",
            ),
        ),
        migrations.AlterField(
            model_name="highlightgallerypage",
            name="intro",
            field=wagtail.fields.RichTextField(
                help_text="1-2 sentences introducing the subject of the page, and explaining why a user should read on.",
                max_length=300,
                verbose_name="introductory text",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerindexpage",
            name="sub_heading",
            field=wagtail.fields.RichTextField(
                help_text="1-2 sentences introducing the subject of the page, and explaining why a user should read on.",
                max_length=300,
                verbose_name="introductory text",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerpage",
            name="sub_heading",
            field=wagtail.fields.RichTextField(
                help_text="1-2 sentences introducing the subject of the page, and explaining why a user should read on.",
                max_length=300,
                verbose_name="introductory text",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerindexpage",
            name="sub_heading",
            field=wagtail.fields.RichTextField(
                help_text="1-2 sentences introducing the subject of the page, and explaining why a user should read on.",
                max_length=300,
                verbose_name="introductory text",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerpage",
            name="sub_heading",
            field=wagtail.fields.RichTextField(
                help_text="1-2 sentences introducing the subject of the page, and explaining why a user should read on.",
                max_length=300,
                verbose_name="introductory text",
            ),
        ),
    ]
