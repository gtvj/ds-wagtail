# Generated by Django 5.0.4 on 2024-04-24 09:20
# etna:allowAlterField

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0104_alter_articlepage_body_alter_focusedarticlepage_body"),
        ("wagtailcore", "0091_remove_revision_submitted_for_moderation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recordarticlepage",
            name="featured_article",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a page to display in the featured area. This can be an Article, Focused Article or Record Article.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
                verbose_name="featured article",
            ),
        ),
    ]
