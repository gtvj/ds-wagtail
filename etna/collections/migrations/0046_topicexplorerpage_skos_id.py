# Generated by Django 4.1.8 on 2023-04-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0045_alter_timeperiodexplorerpage_body_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="topicexplorerpage",
            name="skos_id",
            field=models.CharField(
                blank=True,
                help_text="Used as the identifier for this topic when sending page metadata to the CIIM API.",
                max_length=100,
                verbose_name="SKOS identifier",
            ),
        ),
    ]
