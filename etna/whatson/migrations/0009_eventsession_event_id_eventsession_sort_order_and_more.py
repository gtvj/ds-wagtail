# Generated by Django 4.2.7 on 2024-01-02 09:38

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("whatson", "0008_eventpage_need_to_know_button_link_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventsession",
            name="event_id",
            field=models.CharField(
                blank=True, editable=False, null=True, verbose_name="event ID"
            ),
        ),
        migrations.AddField(
            model_name="eventsession",
            name="sort_order",
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="eventpage",
            name="venue_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("online", "Online"),
                    ("in_person", "In person"),
                    ("hybrid", "Hybrid"),
                ],
                default="in_person",
                max_length=15,
                verbose_name="venue type",
            ),
        ),
        migrations.AlterField(
            model_name="eventsession",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions",
                to="whatson.eventpage",
            ),
        ),
    ]
