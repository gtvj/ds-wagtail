# Generated by Django 4.2.6 on 2023-11-06 15:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0099_alter_articleindexpage_featured_article_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="focusedarticlepage",
            name="author",
        ),
    ]
