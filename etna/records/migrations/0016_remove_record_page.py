# Generated by Django 3.2.9 on 2022-01-12 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('records', '0015_rename_availability_fields'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecordPage',
        ),
    ]
