# Generated by Django 4.2.4 on 2023-08-04 11:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authors", "0006_alter_authortag_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="authorpage",
            name="bio_link",
        ),
        migrations.RemoveField(
            model_name="authorpage",
            name="bio_link_label",
        ),
    ]
