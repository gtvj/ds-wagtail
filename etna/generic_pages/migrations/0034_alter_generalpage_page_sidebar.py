# Generated by Django 5.0.8 on 2024-08-28 17:24
# etna:allowAlterField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("generic_pages", "0033_alter_generalpage_page_sidebar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalpage",
            name="page_sidebar",
            field=models.CharField(
                blank=True,
                choices=[
                    ("contents", "Contents"),
                    ("sections", "Sections"),
                    ("section_tabs", "Section tabs"),
                    ("pages", "Pages"),
                    ("pages_tabs", "Pages tabs"),
                ],
                help_text="Select the sidebar style for this page. For more information, see the <a href='https://nationalarchives.github.io/design-system/components/sidebar/'>sidebar documentation</a>.",
                null=True,
            ),
        ),
    ]
