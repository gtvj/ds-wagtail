# Generated by Django 4.0.8 on 2022-11-02 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('highlights', '0011_closerlookpage_image_library_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='closerlookpage',
            name='related_records',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='highlights.highlightsgallerypage', verbose_name='Related records'),
        ),
    ]
