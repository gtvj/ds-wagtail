# Generated by Django 4.2.2 on 2023-07-05 11:46

from django.db import migrations, models
import django.db.models.deletion
import etna.records.fields
import wagtail.fields
import wagtail.search.index


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("images", "0008_alter_customimagerendition_file"),
        ("highlights", "0003_delete_highlight"),
    ]

    operations = [
        migrations.CreateModel(
            name="Highlight",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "record",
                    etna.records.fields.RecordField(
                        help_text="The record (from CIIM) this highlight corresponds to.",
                        verbose_name="record",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="A descriptive title to use when featuring this record in various places across the site (max length: 200 chars).",
                        max_length=200,
                        verbose_name="title",
                    ),
                ),
                (
                    "dates",
                    models.CharField(
                        blank=True,
                        help_text="Date(s) related to the record (max length: 100 chars).",
                        max_length=100,
                        verbose_name="date(s)",
                    ),
                ),
                (
                    "description",
                    wagtail.fields.RichTextField(
                        help_text="A 100-300 word description of the story of the record and why it is significant.",
                        max_length=900,
                        verbose_name="description",
                    ),
                ),
                (
                    "reference_number",
                    models.CharField(
                        editable=False, max_length=100, verbose_name="reference number"
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(
                        help_text='Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.',
                        max_length=100,
                        verbose_name="image alt text",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "last_updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="last updated at"),
                ),
                (
                    "teaser_image",
                    models.ForeignKey(
                        help_text="Used to render a thumbnail image when featuring this highlight in various places across the site.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.customimage",
                        verbose_name="teaser image",
                    ),
                ),
            ],
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
