# Generated by Django 5.0.7 on 2024-08-07 07:24
# etna:allowAlterField

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authors", "0003_authorindexpage_alert_authorpage_alert"),
        ("images", "0009_alter_customimage_custom_sensitive_image_warning"),
    ]

    operations = [
        migrations.AddField(
            model_name="authorindexpage",
            name="facebook_og_description",
            field=models.TextField(
                blank=True,
                help_text="If left blank, the OpenGraph description will be used.",
                null=True,
                verbose_name="Facebook OpenGraph description",
            ),
        ),
        migrations.AddField(
            model_name="authorindexpage",
            name="facebook_og_image",
            field=models.ForeignKey(
                blank=True,
                help_text="If left blank, the OpenGraph image will be used.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Facebook OpenGraph image",
            ),
        ),
        migrations.AddField(
            model_name="authorindexpage",
            name="facebook_og_title",
            field=models.CharField(
                blank=True,
                help_text="If left blank, the OpenGraph title will be used.",
                max_length=255,
                null=True,
                verbose_name="Facebook OpenGraph title",
            ),
        ),
        migrations.AddField(
            model_name="authorindexpage",
            name="twitter_og_author",
            field=models.CharField(
                blank=True,
                help_text="This will be used if there are no authors of the page. If left blank, the site name will be used.",
                max_length=255,
                null=True,
                verbose_name="Twitter OpenGraph author",
            ),
        ),
        migrations.AddField(
            model_name="authorindexpage",
            name="twitter_og_description",
            field=models.TextField(
                blank=True,
                help_text="If left blank, the OpenGraph description will be used.",
                null=True,
                verbose_name="Twitter OpenGraph description",
            ),
        ),
        migrations.AddField(
            model_name="authorindexpage",
            name="twitter_og_image",
            field=models.ForeignKey(
                blank=True,
                help_text="If left blank, the OpenGraph image will be used.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Twitter OpenGraph image",
            ),
        ),
        migrations.AddField(
            model_name="authorindexpage",
            name="twitter_og_title",
            field=models.CharField(
                blank=True,
                help_text="If left blank, the OpenGraph title will be used.",
                max_length=255,
                null=True,
                verbose_name="Twitter OpenGraph title",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="facebook_og_description",
            field=models.TextField(
                blank=True,
                help_text="If left blank, the OpenGraph description will be used.",
                null=True,
                verbose_name="Facebook OpenGraph description",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="facebook_og_image",
            field=models.ForeignKey(
                blank=True,
                help_text="If left blank, the OpenGraph image will be used.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Facebook OpenGraph image",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="facebook_og_title",
            field=models.CharField(
                blank=True,
                help_text="If left blank, the OpenGraph title will be used.",
                max_length=255,
                null=True,
                verbose_name="Facebook OpenGraph title",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="twitter_og_author",
            field=models.CharField(
                blank=True,
                help_text="This will be used if there are no authors of the page. If left blank, the site name will be used.",
                max_length=255,
                null=True,
                verbose_name="Twitter OpenGraph author",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="twitter_og_description",
            field=models.TextField(
                blank=True,
                help_text="If left blank, the OpenGraph description will be used.",
                null=True,
                verbose_name="Twitter OpenGraph description",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="twitter_og_image",
            field=models.ForeignKey(
                blank=True,
                help_text="If left blank, the OpenGraph image will be used.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Twitter OpenGraph image",
            ),
        ),
        migrations.AddField(
            model_name="authorpage",
            name="twitter_og_title",
            field=models.CharField(
                blank=True,
                help_text="If left blank, the OpenGraph title will be used.",
                max_length=255,
                null=True,
                verbose_name="Twitter OpenGraph title",
            ),
        ),
        migrations.AlterField(
            model_name="authorindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear when this page is shared on social media. This will default to the teaser image if left blank.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="OpenGraph image",
            ),
        ),
        migrations.AlterField(
            model_name="authorpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear when this page is shared on social media. This will default to the teaser image if left blank.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="OpenGraph image",
            ),
        ),
    ]
