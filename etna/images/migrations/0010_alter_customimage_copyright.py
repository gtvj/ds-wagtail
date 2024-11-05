# Generated by Django 5.0.9 on 2024-10-23 13:24
# etna:allowAlterField

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0009_alter_customimage_custom_sensitive_image_warning"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customimage",
            name="copyright",
            field=wagtail.fields.RichTextField(
                blank=True,
                help_text="Credit for images not owned by TNA. Do not include the copyright symbol.",
                max_length=200,
                verbose_name="copyright",
            ),
        ),
    ]
