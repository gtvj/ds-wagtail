# Generated by Django 3.2.9 on 2022-01-12 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0014_add_related_records_and_articles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recordpage',
            old_name='availablility_access_closure_label',
            new_name='availability_access_closure_label',
        ),
        migrations.RenameField(
            model_name='recordpage',
            old_name='availablility_access_display_label',
            new_name='availability_access_display_label',
        ),
        migrations.RenameField(
            model_name='recordpage',
            old_name='availablility_delivery_condition',
            new_name='availability_delivery_condition',
        ),
        migrations.RenameField(
            model_name='recordpage',
            old_name='availablility_delivery_surrogates',
            new_name='availability_delivery_surrogates',
        ),
    ]
