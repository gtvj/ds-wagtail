# Generated by Django 4.0.8 on 2022-11-23 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('highlights', '0003_closerlookpage_search_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closerlookpage',
            name='standfirst',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='highlightsgallerypage',
            name='standfirst',
            field=models.CharField(max_length=350, null=True),
        ),
    ]
