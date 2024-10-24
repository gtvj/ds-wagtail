# Generated by Django 5.0.9 on 2024-10-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0002_etnamedia_chapters"),
    ]

    operations = [
        migrations.AddField(
            model_name="etnamedia",
            name="chapters_file",
            field=models.FileField(
                blank=True, null=True, upload_to="media", verbose_name="chapters_file"
            ),
        ),
        migrations.AddField(
            model_name="etnamedia",
            name="subtitles_file",
            field=models.FileField(
                blank=True, null=True, upload_to="media", verbose_name="subtitles_file"
            ),
        ),
    ]
