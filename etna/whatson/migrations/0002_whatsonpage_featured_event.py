# Generated by Django 4.2.6 on 2023-10-18 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("whatson", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="whatsonpage",
            name="featured_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="whatson.eventpage",
                verbose_name="featured event",
            ),
        ),
    ]
