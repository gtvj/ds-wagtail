# Generated by Django 5.0.7 on 2024-07-30 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0002_alert_uid"),
    ]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="name",
            field=models.CharField(
                default="replace",
                help_text="The name of the alert to display in the CMS, for easier identification.",
                max_length=100,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="alert",
            name="title",
            field=models.CharField(
                help_text="The short title of your alert which will show in bold at the top of the notification banner. E.g. 'Please note' or 'Important information'",
                max_length=50,
            ),
        ),
    ]
