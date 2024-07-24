# Generated by Django 5.0.7 on 2024-07-24 15:44

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("generic_pages", "0027_alter_generalpage_body"),
        ("images", "0008_alter_customimagerendition_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="generalpage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
            ),
        ),
        migrations.AddField(
            model_name="generalpage",
            name="hero_image_caption",
            field=wagtail.fields.RichTextField(
                blank=True,
                help_text="An optional caption for hero images. This could be used for image sources or for other useful metadata.",
                verbose_name="hero image caption (optional)",
            ),
        ),
        migrations.AddField(
            model_name="generalpage",
            name="page_sidebar",
            field=models.CharField(
                blank=True,
                choices=[
                    ("contents", "Contents"),
                    ("sections", "Sections"),
                    ("pages", "Pages"),
                ],
                help_text="Select the sidebar style for this page. For more information, see the <a href='https://nationalarchives.github.io/design-system/components/sidebar/'>sidebar documentation</a>.",
                null=True,
            ),
        ),
    ]
