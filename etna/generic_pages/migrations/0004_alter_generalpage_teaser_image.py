# Generated by Django 4.0.8 on 2023-03-10 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0005_alter_customimage_file_and_more"),
        ("generic_pages", "0003_add_teaser_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalpage",
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
