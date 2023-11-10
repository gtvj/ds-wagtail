# Generated by Django 4.2.6 on 2023-11-02 12:09

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Alert",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("message", wagtail.fields.RichTextField()),
                ("active", models.BooleanField(default=False)),
                (
                    "cascade",
                    models.BooleanField(
                        default=False,
                        verbose_name="Show on current and all child pages",
                    ),
                ),
                (
                    "alert_level",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("medium", "Medium"),
                            ("high", "High"),
                        ],
                        default="low",
                        max_length=6,
                    ),
                ),
            ],
        ),
    ]
