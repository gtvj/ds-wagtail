# Generated by Django 3.1.8 on 2021-06-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_recordpage_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordpage',
            name='arrangement',
            field=models.TextField(blank=True),
        ),
    ]
