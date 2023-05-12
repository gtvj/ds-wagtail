# Generated by Django 4.1.8 on 2023-05-04 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0007_customimage_custom_sensitive_image_warning_and_more"),
        ("articles", "0081_merge_20230504_1135"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordarticlepage",
            name="intro_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Square, rotated image to display in the page introduction",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="intro image",
            ),
        ),
    ]
