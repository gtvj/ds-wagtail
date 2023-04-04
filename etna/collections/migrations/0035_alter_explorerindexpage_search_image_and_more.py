# Generated by Django 4.0.8 on 2023-03-10 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0005_alter_customimage_file_and_more"),
        ("collections", "0034_alter_explorerindexpage_teaser_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="explorerindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="highlightgallerypage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="resultspage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="timeperiodexplorerpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="topicexplorerpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will appear as a promo when this page is shared on social media.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.customimage",
                verbose_name="Search image",
            ),
        ),
    ]
