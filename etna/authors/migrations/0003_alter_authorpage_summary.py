# Generated by Django 5.0.2 on 2024-02-28 13:16

import etna.core.blocks.paragraph
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authors", "0002_authorindexpage_authorpage_authortag_delete_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authorpage",
            name="summary",
            field=etna.core.blocks.paragraph.APIRichTextField(blank=True, null=True),
        ),
    ]
