# Generated by Django 5.1.2 on 2024-12-19 16:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0112_alter_articlepage_body_alter_focusedarticlepage_body"),
    ]

    def migrate_data(apps, schema_editor):
        Article = apps.get_model("articles.ArticlePage")
        FocusedArticle = apps.get_model("articles.FocusedArticlePage")
        RecordArticle = apps.get_model("articles.RecordArticlePage")
        for page in Article.objects.all():
            if page.newly_published_at:
                page.published_date = page.newly_published_at or page.first_published_at or django.utils.timezone.now()
            page.save()
        for page in FocusedArticle.objects.all():
            if page.newly_published_at:
                page.published_date = page.newly_published_at or page.first_published_at or django.utils.timezone.now()
            page.save()
        for page in RecordArticle.objects.all():
            if page.newly_published_at:
                page.published_date = page.newly_published_at or page.first_published_at or django.utils.timezone.now()
            page.save()


    operations = [
        migrations.AddField(
            model_name="articlepage",
            name="published_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="The date the page was published to the public.",
                verbose_name="Published date",
            ),
        ),
        migrations.AddField(
            model_name="focusedarticlepage",
            name="published_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="The date the page was published to the public.",
                verbose_name="Published date",
            ),
        ),
        migrations.AddField(
            model_name="recordarticlepage",
            name="published_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="The date the page was published to the public.",
                verbose_name="Published date",
            ),
        ),
        migrations.RunPython(migrate_data),
    ]
