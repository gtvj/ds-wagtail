# Generated by Django 4.2.5 on 2023-09-25 10:55

from django.db import migrations, models
import django.db.models.deletion


def convert_to_foreign_key(apps, schema_editor):
    FocusedArticlePage = apps.get_model("articles", "FocusedArticlePage")

    for page in FocusedArticlePage.objects.all():
        if page.author:
            page.author = None
            page.save()


class Migration(migrations.Migration):
    dependencies = [
        ("authors", "0002_authorindexpage_authorpage_authortag_delete_author"),
        ("articles", "0097_alter_articlepage_mark_new_on_next_publish_and_more"),
    ]

    operations = [
        migrations.RunPython(convert_to_foreign_key),
        migrations.AlterField(
            model_name="focusedarticlepage",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="focused_articles",
                to="authors.authorpage",
            ),
        ),
    ]
