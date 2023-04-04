# Generated by Django 3.1.8 on 2021-07-02 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
        ("wagtailimages", "0023_add_choose_permissions"),
        ("collections", "0003_add_collection_results_page"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ExplorerPage",
            new_name="ExplorerIndexPage",
        ),
        migrations.RenameModel(
            old_name="CategoryPage",
            new_name="TopicExplorerPage",
        ),
        migrations.AddField(
            model_name="resultspage",
            name="introduction",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resultspage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
        migrations.AddField(
            model_name="explorerindexpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
        migrations.AddField(
            model_name="topicexplorerpage",
            name="teaser_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
        migrations.CreateModel(
            name="TimePeriodExplorerPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("introduction", models.CharField(max_length=200)),
                ("start_year", models.IntegerField()),
                ("end_year", models.IntegerField()),
                (
                    "teaser_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
    ]
